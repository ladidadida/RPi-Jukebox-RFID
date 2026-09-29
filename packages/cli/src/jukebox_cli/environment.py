"""How this jukebox is installed: from a source checkout or as a package."""

import shutil
import sys
from pathlib import Path
from typing import Optional

import jukebox

#: Where releases (wheels) are published
DEFAULT_REPO = 'ladidadida/RPi-Jukebox-RFID'


def checkout() -> Optional[Path]:
    """The repository root when running from a source checkout."""
    root = Path(jukebox.__file__).resolve().parents[4]
    return root if (root / '.git').exists() and (root / 'packages' / 'jukebox').is_dir() else None


def jukebox_executable() -> str:
    candidate = Path(sys.executable).parent / 'jukebox'
    return str(candidate) if candidate.exists() else (shutil.which('jukebox') or 'jukebox')
