"""Where the jukebox keeps its data (``JUKEBOX_HOME``) and its packaged resources.

All runtime data lives below one directory::

    $JUKEBOX_HOME/settings/      configuration, card database, library index, status files
    $JUKEBOX_HOME/audiofolders/  the music library
    $JUKEBOX_HOME/logs/  cache/  playlists/

Relative paths in the configuration are resolved against ``JUKEBOX_HOME``. A leading ``shared/``
(the checkout layout before ``JUKEBOX_HOME`` existed) is dropped, so old configurations keep working.
"""

import os
from importlib import resources
from pathlib import Path
from typing import Optional, Union

HOME_ENV = 'JUKEBOX_HOME'
LEGACY_PREFIX = 'shared'

_home: Optional[Path] = None


def default_home() -> Path:
    xdg_data_home = os.environ.get('XDG_DATA_HOME')
    base = Path(xdg_data_home) if xdg_data_home else Path.home() / '.local' / 'share'
    return base / 'jukebox'


def home() -> Path:
    """The jukebox home: set explicitly, else ``$JUKEBOX_HOME``, else ``$XDG_DATA_HOME/jukebox``."""
    global _home
    if _home is None:
        configured = os.environ.get(HOME_ENV)
        _home = Path(configured).expanduser().resolve() if configured else default_home()
    return _home


def set_home(path: Union[str, Path, None]) -> None:
    """Use ``path`` as home (None: determine it again from the environment)."""
    global _home
    _home = Path(path).expanduser().resolve() if path is not None else None


def resolve(value: Union[str, Path]) -> Path:
    """A configured path: absolute or ``~`` as given, relative ones below the home."""
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    parts = path.parts
    if parts and parts[0] == LEGACY_PREFIX:
        path = Path(*parts[1:]) if len(parts) > 1 else Path('.')
    return home() / path


def settings_dir() -> Path:
    return home() / 'settings'


def resource(*parts: str) -> Path:
    """A file shipped with the jukebox package (default settings, sounds, service templates)."""
    return Path(str(resources.files('jukebox').joinpath('resources', *parts)))
