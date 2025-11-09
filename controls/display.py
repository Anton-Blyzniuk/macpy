import subprocess
import re


class DisplayController:

    def __init__(self, display_id: str) -> None:
        self.display_id = display_id
        self.current_brightness = None

    @property
    def current_resolution(self) -> tuple[int, int]:
        cmd = [
            "bash",
            "-c",
            (
                f'displayplacer list | '
                f'awk -v id="{self.display_id}" \'$0 ~ "Persistent screen id: "id {{f=1}} f && /Resolution:/ {{print $2; exit}}\''
            )
        ]

        try:
            cmd_output = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error running displayplacer command: {e}"
            )
        raw_result = f"{cmd_output.stdout.strip()}".split("x")
        return int(raw_result[0]), int(raw_result[1])


    @property
    def current_refresh_rate(self) -> int:
        cmd = [
            "bash",
            "-c",
            (
                f'displayplacer list | '
                f'awk -v id="{self.display_id}" '
                f'\'$0 ~ "Persistent screen id: "id {{f=1}} '
                f'f && /<-- current mode/ {{for (i=1;i<=NF;i++) if ($i ~ /^hz:/) {{sub("hz:","",$i); print $i; exit}}}}\''
            )
        ]

        try:
            cmd_output = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error running displayplacer command: {e}"
            )

        raw_result = cmd_output.stdout.strip()

        if not raw_result or not raw_result.endswith("hz:"):
            raw_result = raw_result.replace("hz:", "").strip()

        return int(raw_result)

    def _get_current_brightness(self) -> int:
        """
        Under development.
        """
        pass

    def change_resolution(self, width: int, height: int) -> dict:
        """
        ⚠️ Note:
        Not every resolution value will work on every machine.
        You must run `displayplacer list` in Terminal to see which resolutions
        and scaling modes are available for your display before using this method.
        """
        cmd = f'displayplacer "id:{self.display_id} res:{width}x{height} hz:{self.current_refresh_rate} scaling:on"'
        try:
            subprocess.run(
                cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return {
                "status": True,
                "message": f"✅ Display resolution was set to {width}x{height}"
            }

        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Display resolution wasn't changed: {e}"
            }

    def change_refresh_rate(self, refresh_rate: int) -> dict:
        """
        ⚠️ Note:
        Not all refresh rate values will work on every monitor.
        Run `displayplacer list` in Terminal to view all valid refresh rate options
        for your specific display before using this method.
        """
        cur_res = self.current_resolution
        cmd = f'displayplacer "id:{self.display_id} res:{cur_res[0]}x{cur_res[1]} hz:{refresh_rate} scaling:on"'
        try:
            subprocess.run(
                cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return {
                "status": True,
                "message": f"✅ Display refresh rate was set to {refresh_rate}"
            }

        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Display refresh rate wasn't changed: {e}"
            }

    def change_brightness(self, brightness: int) -> None:
        """
        Under development.
        """
        pass


if __name__ == "__main__":
    my_display = DisplayController(
        "37D8832A-2D66-02CA-B9F7-8F30A301B230"
    )
    print(my_display.current_resolution)
    print(my_display.current_refresh_rate)
    # print(my_display.change_resolution(1496,967))
    print(my_display.change_refresh_rate(40))

