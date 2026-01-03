import subprocess


class AppController:

    def force_close_applications(self, app_list: list[str]) -> None:
        for app in app_list:
            cmd = f"""
            osascript -e 'quit app "{app}"' ; \
            pkill -9 -x "{app}" ; \
            ps aux | grep -i "{app}" | grep -v grep | awk '{{print $2}}' | xargs kill -9
            """
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                check=False,
            )


    def close_applications(self, app_list: list[str]) -> None:
        for app in app_list:
            cmd = f"""
            osascript -e 'quit app "{app}"'
            """
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                check=False,
            )


    def close_every_application_except(self, app_list: list[str]) -> None:
        apps_literal = "{" + ",".join(f'"{app}"' for app in app_list) + "}"
        script = f'''
        tell application "System Events"
            -- Only GUI apps with visible UI (skip helpers)
            set appList to (name of every application process whose visible is true)
        end tell

        set excludeList to {apps_literal}

        repeat with appName in appList
            set appNameStr to (appName as text)
            if excludeList does not contain appNameStr then
                try
                    tell application appNameStr to quit
                end try
            end if
        end repeat
        '''

        subprocess.run(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    def open_applications(self, app_list: list[str]) -> None:
        for app in app_list:
            cmd = f'open -a "{app}"'
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                check=False,
            )

    def focus_application(self, app_name: str) -> None:
        subprocess.run(
            f'open -a "{app_name}"',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
            check=False,
        )


if __name__ == "__main__":
    app_controller = AppController()
    app_controller.close_everything_except([
        "Finder",
        "Ghostty",
        "Aerospace",
        "AlDente",
        "Google Chrome"
    ])
