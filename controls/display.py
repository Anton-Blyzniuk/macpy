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
        pass

    def change_resolution(self, width: int, height: int) -> None:
        pass

    def change_refresh_rate(self, refresh_rate: int) -> None:
        pass

    def change_brightness(self, brightness: int) -> None:
        pass


if __name__ == "__main__":
    my_display = DisplayController(
        "37D8832A-2D66-02CA-B9F7-8F30A301B230"
    )
    print(my_display.current_resolution)
    print(my_display.current_refresh_rate)
