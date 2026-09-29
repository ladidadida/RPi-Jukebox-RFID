"""The core modules the daemon always starts. Order is irrelevant, ``requires`` decides."""

from jukebox.input_devices import InputDevices
from jukebox.jingle import Jingle
from jukebox.library.module import Library
from jukebox.player.module import Player
from jukebox.rfid.cards import Cards
from jukebox.rfid.reader import Rfid
from jukebox.system import System
from jukebox.timers import Timers
from jukebox.volume import Volume

CORE_MODULES = [System, Library, Player, Volume, Timers, Jingle, InputDevices, Cards, Rfid]
