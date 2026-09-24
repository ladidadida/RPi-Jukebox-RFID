import os
import re
import logging
import jukebox.cfghandler
from typing import Optional
from .playcontentcallback import PlayContentCallbacks, PlayCardState


logger = logging.getLogger('jb.player')
cfg = jukebox.cfghandler.get_handler('jukebox')

#: Callback handler for card-triggered playback. This belongs to the player
#: facade rather than to a specific playback backend.
play_card_callbacks = PlayContentCallbacks[PlayCardState]('play_card_callbacks', logger)


def _get_music_library_path(conf_file):
    """Parse the music directory from the mpd.conf file"""
    pattern = re.compile(r'^\s*music_directory\s*"(.*)"', re.I)
    directory = None
    with open(conf_file, 'r') as f:
        for line in f:
            res = pattern.match(line)
            if res:
                directory = res.group(1)
                break
        else:
            logger.error(f"Could not find music library path in {conf_file}")
    logger.debug(f"MPD music lib path = {directory}; from {conf_file}")
    return directory


class MusicLibPath:
    """Determine the music library directory.

    Primarily from `player.music_library_path` config (backend-agnostic). Falls back to parsing
    `music_directory` out of mpd.conf only when the mpd backend is active and no explicit path was
    configured -- keeps existing mpd installs working without a migration step.
    """
    def __init__(self):
        self._music_library_path = cfg.getn('player', 'music_library_path', default=None)
        if self._music_library_path is not None:
            return
        if cfg.getn('player', 'backend', default='local_audio') != 'mpd':
            return
        mpd_conf_file = cfg.setndefault('playermpd', 'mpd_conf', value='~/.config/mpd/mpd.conf')
        try:
            self._music_library_path = _get_music_library_path(os.path.expanduser(mpd_conf_file))
        except Exception as e:
            logger.error(f"Could not determine music library directory from '{mpd_conf_file}'")
            logger.error(f"Reason: {e.__class__.__name__}: {e}")

    @property
    def music_library_path(self):
        return self._music_library_path


# ---------------------------------------------------------------------------


_MUSIC_LIBRARY_PATH: Optional[MusicLibPath] = None


def get_music_library_path():
    """Get the music library path"""
    global _MUSIC_LIBRARY_PATH
    if _MUSIC_LIBRARY_PATH is None:
        _MUSIC_LIBRARY_PATH = MusicLibPath()
    return _MUSIC_LIBRARY_PATH.music_library_path
