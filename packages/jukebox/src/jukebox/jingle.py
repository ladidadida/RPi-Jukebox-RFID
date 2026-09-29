"""The jingle core module: startup and shutdown sounds, and playing a sound on demand."""

import logging
import signal
import threading
from pathlib import Path

from jukebox.audio_output import play_file
from jukebox.contract import CoreModule, OperationError, action

logger = logging.getLogger('jb.jingle')

SHUTDOWN_SOUND_TIMEOUT = 3.0


class Jingle(CoreModule):
    """Plays the startup sound when ready and the shutdown sound when stopping."""

    name = 'jingle'
    interface_version = '1.0'
    concurrency = 'threadsafe'

    def __init__(self):
        self._ctx = None
        self._executor = None
        self._stopping = threading.Event()

    def start(self, ctx) -> None:
        self._ctx = ctx
        self._executor = ctx.executor('sound')

    def _volume(self) -> int:
        volume = self._ctx.config.get('volume', default=None)
        return 100 if volume is None else max(0, min(100, int(volume)))

    def _play(self, sound: str) -> None:
        try:
            play_file(sound, self._volume(), should_stop=self._stopping.is_set)
        except Exception as error:
            logger.error(f"Could not play '{sound}': {error.__class__.__name__}: {error}")

    def ready(self) -> None:
        sound = self._ctx.config.get('startup_sound', default=None)
        if sound:
            self._executor.submit(self._play, sound)

    def stop(self):
        sound = self._ctx.config.get('shutdown_sound', default=None)
        from jukebox.daemon import shutdown_signal
        if sound and shutdown_signal() != signal.SIGINT:
            done = threading.Thread(target=self._play, args=(sound,), name='jingle.shutdown', daemon=True)
            done.start()
            done.join(SHUTDOWN_SOUND_TIMEOUT)
        self._stopping.set()
        return []

    @action()
    def play(self, sound: str) -> None:
        """Play a sound file (path relative to the jukebox directory or absolute)."""
        if not Path(sound).expanduser().is_file():
            raise OperationError(404, 'unknown_sound', f"Sound file '{sound}' not found")
        self._executor.submit(self._play, str(Path(sound).expanduser()))
