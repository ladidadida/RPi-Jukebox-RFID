import logging

import components.player
import jukebox.cfghandler
import jukebox.registry as registry
import misc

from .backends.mpd import PlayerMPD
from .coordinator import PlayerCoordinator


logger = logging.getLogger('jb.player')
cfg = jukebox.cfghandler.get_handler('jukebox')


def initialize_mpd_player() -> PlayerCoordinator:
    """Create the coordinator with MPD as its sole backend and register it as 'player.ctrl'."""
    player_ctrl = PlayerCoordinator(components.player.play_card_callbacks)
    player_ctrl.register_backend('mpd', PlayerMPD())
    registry.register(player_ctrl, name='ctrl', package='player')

    if cfg.setndefault('playermpd', 'library', 'update_on_startup', value=True):
        player_ctrl.update()

    check_user_rights = cfg.setndefault(
        'playermpd', 'library', 'check_user_rights', value=True
    )
    if check_user_rights is True:
        music_library_path = components.player.get_music_library_path()
        if music_library_path is not None:
            logger.info(f"Change user rights for {music_library_path}")
            misc.recursive_chmod(music_library_path, mode_files=0o666, mode_dirs=0o777)

    return player_ctrl
