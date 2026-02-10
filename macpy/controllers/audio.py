from macpy.core import BaseController, CommandResult



class AudioController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.volume_sate: int|None = None

    def set_volume(self, volume: int) -> CommandResult:
        result = self._execute(
            [
                "osascript",
                "-e",
                f"set volume output volume {volume}"
            ],
            raise_on_error=True
        )
        self.volume_sate = volume
        return result
