from macpy.core import BaseController, CommandResult
from macpy.utils import fit_number_in_range_or_raise_an_error


class DisplayController(BaseController):
    KEY_PRES_FOR_LOWEST_BRIGHTNESS = 16

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.brightness_state: int|None = None

    @classmethod
    def _brightness_up(cls) -> CommandResult:
        return cls._execute(
            [
                "osascript",
                "-e",
                'tell application "System Events" to key code 144'
            ],
            raise_on_error=True
        )

    @classmethod
    def _brightness_down(cls) -> CommandResult:
        return cls._execute(
            [
                "osascript",
                "-e",
                'tell application "System Events" to key code 145'
            ],
            raise_on_error = True
        )

    def calibrate_brightness(self) -> CommandResult:
        for _ in range(self.KEY_PRES_FOR_LOWEST_BRIGHTNESS):
            DisplayController._brightness_down()
        self.brightness_state = 0

        return CommandResult(
            success=True,
            message="Brightness calibrated."
        )

    def set_brightness(self, brightness: int, **kwargs) -> CommandResult:
        fit_number_in_range_or_raise_an_error(
            number=brightness,
            lower_bound=0,
            upper_bound=100,
            raise_on_error=False
        )

        if not kwargs.get("do_not_calibrate"):
            if self.brightness_state != 0:
                self.calibrate_brightness()

        for _ in range(round((16 / 100) * brightness)):
            self._brightness_up()
        self.brightness_state = brightness

        return CommandResult(
            success=True,
            message=f"Brightness set to {brightness}."
        )

