"""Player start-up/shutdown, called explicitly by jukebox.daemon (no plugin system)."""

from .mpd_plugin import initialize_mpd_player

player_ctrl = None


def start():
    global player_ctrl
    player_ctrl = initialize_mpd_player()
    return player_ctrl


def stop():
    if player_ctrl is not None:
        return player_ctrl.exit()
