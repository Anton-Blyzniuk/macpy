from macpy.controllers import BaseController, CommandResult

class ShellController(BaseController):
    def execute_cli_command(
            self,
            command_instructions: list[str]
    ) -> CommandResult:
        return self._execute(
            command_instructions,
            raise_on_error=True
        )

    def execute_apple_shortcut(
            self,
            shortcut_name: str
    ) -> CommandResult:
        return self._execute(
            [
                "shortcuts",
                "run",
                shortcut_name
            ],
            raise_on_error=True
        )