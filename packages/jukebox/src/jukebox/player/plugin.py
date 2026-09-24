"""Player start-up/shutdown, called explicitly by jukebox.daemon (no plugin system).

Selects a playback backend module by `player.backend` config, mirroring how
`jukebox.rfid.reader` dynamically loads a hardware module by name.
"""

import importlib
import logging

import jukebox.cfghandler

logger = logging.getLogger('jb.player')
cfg = jukebox.cfghandler.get_handler('jukebox')

#: Backend name -> module exposing `initialize() -> PlayerCoordinator`.
_BACKEND_MODULES = {
    'local_audio': 'jukebox.player.backends.local_audio',
    'mpd': 'jukebox.player.mpd_plugin',
}

#: Backend name -> pyproject.toml extra providing its dependencies. Only backends with their own
#: extra are listed here -- local_audio's deps (av, sounddevice) are unconditional core deps.
_BACKEND_EXTRAS = {
    'mpd': 'mpd',
}

player_ctrl = None


def start():
    global player_ctrl
    name = cfg.setndefault('player', 'backend', value='local_audio')
    try:
        module_path = _BACKEND_MODULES[name]
    except KeyError:
        raise ValueError(
            f"Unknown player backend '{name}'. Available: {list(_BACKEND_MODULES)}"
        ) from None
    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        extra = _BACKEND_EXTRAS.get(name)
        hint = f"uv sync --extra {extra}" if extra else "uv sync"
        raise RuntimeError(
            f"Player backend '{name}' is missing a dependency ({exc}). Install with: {hint}"
        ) from exc
    except OSError as exc:
        # A native library the backend's Python deps bind to (e.g. libportaudio2 for
        # local_audio's sounddevice) failed to load -- this is a missing system package, not a
        # missing Python/uv extra.
        raise RuntimeError(
            f"Player backend '{name}' failed to load a required system library: {exc}"
        ) from exc
    logger.info(f"Starting player backend '{name}'")
    player_ctrl = module.initialize()
    return player_ctrl


def stop():
    if player_ctrl is not None:
        return player_ctrl.exit()
