"""The core modules the daemon always starts. Order is irrelevant, ``requires`` decides."""

from jukebox.player.module import Player
from jukebox.rfid.cards import Cards
from jukebox.rfid.reader import Rfid
from jukebox.system import System

CORE_MODULES = [System, Player, Cards, Rfid]
