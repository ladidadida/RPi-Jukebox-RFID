import logging

import jukebox.player
import jukebox.cfghandler
import jukebox.misc as misc

from .backends.mpd import PlayerMPD


logger = logging.getLogger('jb.player')
cfg = jukebox.cfghandler.get_handler('jukebox')


def create_mpd_backend() -> PlayerMPD:
    """Create the MPD backend and apply the playermpd startup options."""
    backend = PlayerMPD(host=cfg.getn('playermpd', 'host', default='localhost'),
                        status_file=cfg.getn('playermpd', 'status_file',
                                             default='shared/settings/music_player_status.json'))
    if cfg.setndefault('playermpd', 'library', 'update_on_startup', value=True):
        backend.update()

    check_user_rights = cfg.setndefault(
        'playermpd', 'library', 'check_user_rights', value=True
    )
    if check_user_rights is True:
        music_library_path = jukebox.player.get_music_library_path()
        if music_library_path is not None:
            logger.info(f"Change user rights for {music_library_path}")
            misc.recursive_chmod(music_library_path, mode_files=0o666, mode_dirs=0o777)

    return backend
