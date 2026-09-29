"""The system core module: version information, logs and web app settings."""

import logging
import logging.handlers
import os
import time
from typing import Literal, Optional

from pydantic import BaseModel

import jukebox
import jukebox.cfghandler
from jukebox.contract import CoreModule, action, event, query
from jukebox.daemon import get_jukebox_daemon

logger = logging.getLogger('jb.system')
cfg = jukebox.cfghandler.get_handler('jukebox')

LOG_TOPIC = 'system.log'


class SystemInfo(BaseModel):
    version: str
    git_state: str
    started_at: str


class LogMessage(BaseModel):
    message: str


class AppSettings(BaseModel):
    show_covers: bool = True


class AppSettingsUpdate(BaseModel):
    show_covers: Optional[bool] = None


def _read_log(handler_name: str) -> str:
    content = "No file handles configured"
    for h in logging.getLogger('jb').handlers:
        if not isinstance(h, logging.handlers.RotatingFileHandler):
            continue
        content = f"No file handler with name {handler_name} configured"
        if h.name != handler_name:
            continue
        try:
            if os.path.getsize(h.baseFilename) == 0:
                return (f"Log file {h.baseFilename} is empty. (Is the RotatingFileHandler configured as "
                        f"handler sink for jb in logger.yaml?)")
            mtime = os.path.getmtime(h.baseFilename)
            stime = get_jukebox_daemon().start_time
            # 3 seconds tolerance between file creation and recording the start time
            if mtime - stime < -3:
                return (f"Log file {h.baseFilename} too old for this Jukebox start! "
                        f"Is the RotatingFileHandler configured as handler sink for jb in logger.yaml?")
            with open(h.baseFilename) as stream:
                return stream.read()
        except Exception as e:
            content = f"{e.__class__.__name__}: {e}"
            logger.error(content)
        break
    return content


class System(CoreModule):
    """Version information, log files and web app settings."""

    name = 'system'
    interface_version = '1.0'

    info = event('info', SystemInfo)
    #: Published by jukebox.misc.loggingext.PubStreamHandler when configured in logger.yaml
    log = event('log', LogMessage)

    def start(self, ctx) -> None:
        self._ctx = ctx
        ctx.publish(self.info, self.get_info())

    @query(path='/info')
    def get_info(self) -> SystemInfo:
        """Version, git state and start time of the jukebox."""
        daemon = get_jukebox_daemon()
        return SystemInfo(version=jukebox.version(), git_state=daemon.git_state,
                          started_at=time.ctime(daemon.start_time))

    @query(path='/log')
    def get_log(self, kind: Literal['debug', 'error'] = 'debug') -> str:
        """Content of the debug or error log file of this run."""
        return _read_log(f'{kind}_file_handler')

    @query(path='/api/v1/settings')
    def get_app_settings(self) -> AppSettings:
        """Web app settings."""
        return AppSettings(show_covers=cfg.setndefault('webapp', 'show_covers', value=True))

    @action(method='PUT', path='/api/v1/settings')
    def set_app_settings(self, settings: AppSettingsUpdate) -> None:
        """Change web app settings; fields left out stay unchanged."""
        for key, value in settings.model_dump(exclude_none=True).items():
            cfg.setn('webapp', key, value=value)

    @action()
    def noop(self, message: str = '') -> None:
        """Do nothing (logs ``message`` as a warning if given)."""
        if message:
            logger.warning(message)
