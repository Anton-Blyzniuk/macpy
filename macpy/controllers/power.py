from macpy.core import BaseController, CommandResult


class PowerController(BaseController):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.low_power_mode_state: bool|None = None

    def low_power_mode(self, activate: bool = True) -> CommandResult:
        result = self._execute(
            [
                "sudo",
                "pmset",
                "-a",
                "lowpowermode",
                "1" if activate else "0",
            ],
            raise_on_error=True,
        )
        self.low_power_mode_state = activate
        return result