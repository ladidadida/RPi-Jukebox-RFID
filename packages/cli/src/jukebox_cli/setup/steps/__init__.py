from typing import List

from jukebox_cli.setup.base import Step
from jukebox_cli.setup.steps.extras import AudioStep, AutohotspotStep, KioskStep, MpdStep, SambaStep
from jukebox_cli.setup.steps.jukebox import PluginsStep, RfidStep, ServiceStep
from jukebox_cli.setup.steps.system import BootStep, PackagesStep, RaspberryPiStep, WelcomeStep


def all_steps() -> List[Step]:
    """In the order they run (questions are asked in the same order)."""
    return [PackagesStep(), RaspberryPiStep(), MpdStep(), PluginsStep(), ServiceStep(), AudioStep(), SambaStep(),
            RfidStep(), KioskStep(), AutohotspotStep(), BootStep(), WelcomeStep()]
