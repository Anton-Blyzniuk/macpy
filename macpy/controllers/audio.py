from macpy.controllers import BaseController, CommandResult
from macpy.utils import fit_number_in_range_or_raise_an_error


class AudioController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.volume_sate: int|None = None

    def set_volume(self, volume: int) -> CommandResult:
        volume = fit_number_in_range_or_raise_an_error(
            number=volume,
            lower_bound=0,
            upper_bound=100,
            raise_on_error=False
        )
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
