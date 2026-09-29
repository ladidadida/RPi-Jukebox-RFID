"""Player backend using an external MPD server.

Enable with ``player.backend: mpd`` and::

    plugins:
      mpd:
        host: localhost
        status_file: shared/settings/music_player_status.json
        library:
          update_on_startup: true
          check_user_rights: true
"""

import logging

import jukebox.cfghandler
import jukebox.misc as misc
import jukebox.player
from jukebox.contract import Plugin

logger = logging.getLogger('jb.mpd')
cfg_main = jukebox.cfghandler.get_handler('jukebox')

DEFAULTS = {
    'host': 'localhost',
    'status_file': 'shared/settings/music_player_status.json',
    'library': {'update_on_startup': True, 'check_user_rights': True},
}


def _setting(ctx, *keys):
    """Own config section first, then the pre-plugin ``playermpd`` section, then the default."""
    missing = object()
    value = ctx.config.get(*keys, default=missing)
    if value is missing:
        value = cfg_main.getn('playermpd', *keys, default=missing)
    if value is missing:
        value = DEFAULTS
        for key in keys:
            value = value[key]
    return value


class Mpd(Plugin):
    """Registers the ``mpd`` player backend."""

    name = 'mpd'
    interface_version = '1.0'
    requires = {'player': '>=1.0,<2'}

    def start(self, ctx) -> None:
        from jukebox_plugin_mpd.backend import PlayerMPD

        backend = PlayerMPD(host=_setting(ctx, 'host'), status_file=_setting(ctx, 'status_file'))
        if _setting(ctx, 'library', 'update_on_startup'):
            backend.update()
        if _setting(ctx, 'library', 'check_user_rights'):
            music_library_path = jukebox.player.get_music_library_path()
            if music_library_path is not None:
                logger.info(f"Change user rights for {music_library_path}")
                misc.recursive_chmod(music_library_path, mode_files=0o666, mode_dirs=0o777)
        ctx.modules.player.backends.register('mpd', backend)
