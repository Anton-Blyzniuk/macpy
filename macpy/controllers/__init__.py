from macpy.controllers.base import BaseController
from macpy.controllers.result import CommandResult

from macpy.controllers.audio import AudioController
from macpy.controllers.network import NetworkController
from macpy.controllers.display import DisplayController
from macpy.controllers.power import PowerController
from macpy.controllers.apps import AppController
from macpy.controllers.desktop import DesktopController
from macpy.controllers.shell import ShellController

__available_controllers__ = [
    AudioController,
    NetworkController,
    DisplayController,
    PowerController,
    AppController,
    DesktopController,
    ShellController,
]