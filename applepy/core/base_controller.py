import subprocess
from applepy.core import CommandResult


class BaseController:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    @staticmethod
    def _execute(
            command: list[str] | str,
            success_message: bool=None,
            error_message: bool=None,
            raise_on_error: bool=None,
            capture_output: bool=None,
            **kwargs
    ) -> CommandResult:
        try:
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL if not capture_output else None,
                stderr=subprocess.DEVNULL if not capture_output else None,
                capture_output=capture_output if capture_output else False,
                **kwargs,
            )

            if kwargs.get("restart_dock"):
                subprocess.run(["killall", "Dock"], check=True)

            return CommandResult(
                success=True,
                message=success_message if success_message else f"success -> {command}",
                output=result,
            )

        except subprocess.CalledProcessError as e:
            if raise_on_error:
                raise Exception(e)
            return CommandResult(
                success=False,
                message=error_message if error_message else f"failed -> {command} -> {e}",
            )
