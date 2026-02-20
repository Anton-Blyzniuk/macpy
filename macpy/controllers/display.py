from macpy.core import BaseController, CommandResult
from macpy.utils import fit_number_in_range_or_raise_an_error
from macpy.interface import CodeGeneratorMixin
from macpy import settings


class DisplayController(BaseController, CodeGeneratorMixin):
    KEY_PRES_FOR_LOWEST_BRIGHTNESS = 16

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.display_id: str = settings.DISPLAY_ID
        self.brightness_state: int|None = None

    @property
    def current_refresh_rate(self) -> int:
        result = self._execute(
            [
                "bash",
                "-c",
                (
                    f'displayplacer list | '
                    f'awk -v id="{self.display_id}" '
                    f'\'$0 ~ "Persistent screen id: "id {{f=1}} '
                    f'f && /<-- current mode/ {{for (i=1;i<=NF;i++) if ($i ~ /^hz:/) {{sub("hz:","",$i); print $i; exit}}}}\''
                )
            ],
            raise_on_error=True,
            capture_output=True,
            text=True,
        )

        raw_result = result.output.stdout.strip()

        if not raw_result or not raw_result.endswith("hz:"):
            raw_result = raw_result.replace("hz:", "").strip()
        return int(raw_result)

    @property
    def current_resolution(self) -> tuple[int, int]:
        result = self._execute(
            [
                "bash",
                "-c",
                (
                    f'displayplacer list | '
                    f'awk -v id="{self.display_id}" \'$0 ~ "Persistent screen id: "id {{f=1}} f && /Resolution:/ {{print $2; exit}}\''
                )
            ],
            raise_on_error=True,
            capture_output=True,
            text=True,
        )
        raw_result = f"{result.output.stdout.strip()}".split("x")
        return int(raw_result[0]), int(raw_result[1])


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
            raise_on_error = True,
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
        brightness = fit_number_in_range_or_raise_an_error(
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

    def set_resolution(self, width: int, height: int) -> CommandResult:
        return self._execute(
            f'displayplacer "id:{self.display_id} res:{width}x{height} hz:{self.current_refresh_rate} scaling:on"',
            raise_on_error=True,
            shell=True,
        )

    def set_refresh_rate(self, refresh_rate: int) -> CommandResult:
        cur_res = self.current_resolution
        return self._execute(
            f'displayplacer "id:{self.display_id} res:{cur_res[0]}x{cur_res[1]} hz:{refresh_rate} scaling:on"',
            raise_on_error=True,
            shell=True,
        )
