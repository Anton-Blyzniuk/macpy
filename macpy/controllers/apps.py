from macpy.core import BaseController, CommandResult
from macpy.interface import CodeGeneratorMixin


class AppController(BaseController, CodeGeneratorMixin):

    @property
    def running_apps(self) -> list[str]:
        result = self._execute(
            [
                "osascript",
                "-e",
                'tell application "System Events" to get name of (application processes whose background only is false)'
            ],
            capture_output=True,
            text=True,
        )
        apps = [app.strip() for app in result.output.stdout.strip().split(",")]
        return apps

    def open(self, app: str) -> CommandResult:
        return self._execute(
            [
                "osascript",
                "-e",
                f'tell application "{app}" to activate'
            ],
            raise_on_error=True
        )

    def close(self, app: str, force: bool = False) -> CommandResult:
        return self._execute(
            [
                "osascript", "-e", f'tell application "{app}" to quit'
            ]
            if not force else
            [
                "pkill", "-9", "-f", app
            ],
            raise_on_error=True
        )

    def open_applications(self, app_list: list[str]) -> CommandResult:
        for app in app_list:
            self.open(app)
        return CommandResult(
            success=True,
            message=f"{app_list} were opened.",
        )

    def close_applications(self, app_list: list[str], force: bool = False) -> CommandResult:
        for app in app_list:
            self.close(app, force=force)
        return CommandResult(
            success=True,
            message=f"{app_list} were closed.",
        )

    def close_all_applications(
            self,
            ignore_apps : list[str] = None,
            force: bool = False,
            apps_to_force: list[str] = None
    ) -> CommandResult:
        ignore_apps = ignore_apps or []
        apps_to_force = apps_to_force or []

        for app in self.running_apps:
            if app in ignore_apps:
                continue

            app_force = force or (app in apps_to_force)
            self.close(app, force=app_force)

        return CommandResult(
            success=True,
            message=f"All apps were closed except: {ignore_apps}",
        )
