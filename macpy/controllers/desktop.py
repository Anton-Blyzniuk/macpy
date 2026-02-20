from macpy.core import BaseController, CommandResult
from macpy.interface import CodeGeneratorMixin


class DesktopController(BaseController, CodeGeneratorMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_wallpaper: str|None = None

    def set_wallpaper(self, path_to_image: str) -> CommandResult:
        return self._execute(
            [
                "osascript",
                "-e",
                f'tell application "System Events" to set picture of every desktop to "{path_to_image}"'
            ],
            restart_dock=True,
            raise_on_error=True
        )
