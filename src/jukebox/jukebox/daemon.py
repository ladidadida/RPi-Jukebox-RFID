# -*- coding: utf-8 -*-
import threading
import os
import sys
import signal
import logging
import time
import atexit
from typing import (Optional)

from misc import flatten
import jukebox.registry as registry
import jukebox.utils
import jukebox.publishing as publishing
from jukebox.api import ApiServer
from jukebox.rpc.server import RpcServer
from jukebox.NvManager import nv_manager

import jukebox
import jukebox.cfghandler

logger = logging.getLogger('jb.daemon')
cfg = jukebox.cfghandler.get_handler('jukebox')


@atexit.register
def log_active_threads():
    """This functions is registered with atexit very early, meaning it will be run very late. It is the best guess to
    evaluate which Threads are still running (and probably shouldn't be)

    This function is registered before all the components and their dependencies are loaded"""
    logger.debug(f"Active Threads = {threading.enumerate()}")


class JukeBox:
    def __init__(self, configuration_file: str, write_artifacts: bool):
        # Set up the signal listeners
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self._start_time = time.time()
        logger.info(f"Starting Jukebox Daemon (Version {jukebox.version()})")

        self._git_state = jukebox.utils.get_git_state()
        logger.info(f"Git state: {self._git_state}")

        self.nvm = nv_manager()
        self._signal_cnt = 0
        self.rpc_server = None
        self.api_server = None
        jukebox.cfghandler.load_yaml(cfg, configuration_file)

        self.write_artifacts = write_artifacts

        logger.info("Welcome to " + cfg.getn('system', 'box_name', default='Jukebox Version 3'))
        logger.info(f"Time of start: {time.ctime(self._start_time)}")

    @property
    def start_time(self):
        return self._start_time

    @property
    def git_state(self):
        return self._git_state

    def signal_handler(self, esignal, frame):
        """Signal handler for orderly shutdown

        On first Ctrl-C (or SIGTERM) orderly shutdown procedure is embarked upon. It gets allocated a time-out!
        On third Ctrl-C (or SIGTERM), this is interrupted and there will be a hard exit!
        """
        # systemd: By default, a SIGTERM is sent, followed by 90 seconds of waiting followed by a SIGKILL.
        # Pressing Ctrl-C gives SIGINT
        self._signal_cnt += 1
        timeout: float = 5.0
        time_start = time.time_ns()
        msg = f"Received signal '{signal.Signals(esignal).name}'. Count = {self._signal_cnt}"
        print(msg)
        logger.debug(msg)
        if self._signal_cnt == 1:
            # Put the shutdown procedure into a thread, so we can make a time-out on it
            # Cannot use threading.Timer for the timeout, as sys.exit() must be called from main thread
            t = threading.Thread(target=self.exit_gracefully, args=[esignal, timeout], daemon=True, name="ShutdownThread")
            t.start()
            t.join(timeout)
            if t.is_alive():
                msg = f"Shutdown handler timed out after {timeout} s "
                print(f"Shutdown incomplete. {msg}. Terminating now forcefully!")
                print(f"Active Threads = {threading.enumerate()}")
                logger.error(msg)
                # Let's see which threads did not exit properly in time
                logger.error(f"Active Threads = {threading.enumerate()}")
                sys.exit(1)
            logger.info(f"Shutdown time: {((time.time_ns() - time_start) / 1000000.0):.3f} ms")
            sys.exit(0)
        elif self._signal_cnt == 2:
            print("Waiting for closing down procedure to complete. Pressing Ctrl-C again will close Jukebox down immediately.")
        if self._signal_cnt == 3:
            sys.exit(1)

    def exit_gracefully(self, esignal, timeout):
        # Imported lazily: these components import jukebox.daemon.get_jukebox_daemon at module level,
        # so importing them at daemon.py module scope would be circular.
        import components.publishing
        import components.player.plugin
        import components.rfid.cards
        import components.rfid.reader

        msg = f"Closing down JukeBox {cfg.getn('system', 'box_name', default='Unnamed')}"
        print(msg)
        logger.info(msg)
        # (1) Stop taking commands from RPC
        if self.rpc_server is not None:
            self.rpc_server.terminate()
        if self.api_server is not None:
            self.api_server.terminate()
        # (2) Stop the music
        registry.call_ignore_errors('player', 'ctrl', 'stop')
        # (3) Shut down the explicitly wired components (see run()) in reverse start-up order,
        # collecting whatever threads they return so we can wait for them below.
        # Some functions may return None or nested lists: flatten and filter those.
        shutdown_results = [
            components.rfid.reader.stop_readers(signal_id=esignal),
            components.rfid.cards.stop(signal_id=esignal),
            components.player.plugin.stop(),
            components.publishing.stop(signal_id=esignal),
        ]
        thread_list = list(filter(lambda x: x is not None, flatten(shutdown_results)))
        # (4) Save all nonvolatile data
        self.nvm.save_all()
        cfg.save(only_if_changed=True)
        # (5) Wait for open threads to close
        # Note: Not waiting for ALL open threads, only for those threads returned by the shutdown
        # calls in (3) above.
        logger.debug(f"Waiting {timeout}s for component shutdown threads to complete: {thread_list}")
        for t in thread_list:
            t.join()

        logger.debug("All component shutdown threads closed")
        # (6) Say goodbye
        msg = "All done. Hear you soon!"
        print(msg)
        logger.info(msg)

    def run(self):
        time_start = time.time_ns()

        # Imported lazily: components.misc imports jukebox.daemon.get_jukebox_daemon at module level,
        # so importing them at daemon.py module scope would be circular.
        import components.misc
        import components.publishing
        import components.player.plugin
        import components.rfid.cards
        import components.rfid.reader

        # Explicitly wire up the components we need (no plugin system, see
        # documentation/developers/roadmap-core-architecture.md). Order matters: publishing must be
        # running before anything else sends messages; the card database must be loaded before the
        # RFID reader starts scanning.
        components.publishing.register()
        components.publishing.start()
        components.misc.register()
        components.player.plugin.start()
        components.rfid.cards.register()
        components.rfid.cards.start()
        components.rfid.reader.start_readers()

        publishing.get_publisher().send('core.started_at', time.ctime(self._start_time))
        publishing.get_publisher().send('core.git_state', self._git_state)

        self.rpc_server = RpcServer()
        self.api_server = ApiServer()
        self.api_server.start_and_wait()

        logger.info(f"Start-up time: {((time.time_ns() - time_start) / 1000000.0):.3f} ms")

        if self.write_artifacts:
            # This writes out
            # rpc_command_reference.txt
            # rpc_command_alias_reference.txt

            artifacts_dir = '../../shared/artifacts/'

            try:
                os.mkdir(artifacts_dir)
            except FileExistsError:
                pass

            with open(os.path.join(artifacts_dir, 'rpc_command_reference.txt'), 'w') as stream:
                registry.dump_registry(stream)

            # Write reference of command shortcuts
            with open(os.path.join(artifacts_dir, 'rpc_command_alias_reference.txt'), 'w') as stream:
                jukebox.utils.generate_cmd_alias_reference(stream)

        # Start the RPC Server
        self.rpc_server.run()


class JukeBoxBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, *args, **kwargs):
        if not self._instance:
            self._instance = JukeBox(*args, **kwargs)
        return self._instance


_JUKEBOX_BUILDER: Optional[JukeBoxBuilder] = None


def get_jukebox_daemon(*args, **kwargs):
    global _JUKEBOX_BUILDER
    if _JUKEBOX_BUILDER is None:
        _JUKEBOX_BUILDER = JukeBoxBuilder()
    return _JUKEBOX_BUILDER(*args, **kwargs)
