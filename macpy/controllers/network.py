from macpy.core import BaseController, CommandResult
from macpy.interface import CodeGeneratorMixin


class NetworkController(BaseController, CodeGeneratorMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.wifi_state: bool|None = None
        self.bluetooth_state: bool|None = None

    def activate_wifi(self, activate: bool = True, **kwargs) -> CommandResult:
        device_name = kwargs["device_name"] if kwargs.get("device_name") else "en0"
        result = self._execute(
            [
                "networksetup",
                "-setairportpower",
                device_name,
                "on" if activate else "off",
            ],
            raise_on_error=True
        )
        self.wifi_state = activate
        return result

    def activate_bluetooth(self, activate: bool = True) -> CommandResult:
        result = self._execute(
            [
                "blueutil",
                "--power",
                "1" if activate else "0",
            ],
            raise_on_error=True
        )
        self.bluetooth_state = activate
        return result

