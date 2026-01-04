import os
import subprocess
import re


class SystemController:

    @staticmethod
    def wi_fi(activate: bool = True) -> None:
        device_name = "en0"
        try:
            state = "on" if activate else "off"
            subprocess.run(
                ["networksetup", "-setairportpower", device_name, state],
                check=True
            )
            print(f"✅ Wi-Fi {'enabled' if activate else 'disabled'}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to change Wi-Fi state: {e}")


    @staticmethod
    def bluetooth(activate: bool = True) -> None:
        try:
            state = "1" if activate else "0"
            subprocess.run(
                ["blueutil", "--power", state],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Bluetooth {'enabled' if activate else 'disabled'}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to change Bluetooth state: {e}")


    @staticmethod
    def low_power_mode(activate: bool = True) -> None:
        try:
            state = "1" if activate else "0"
            subprocess.run(
                ["sudo", "pmset", "-a", "lowpowermode", state],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Low Power Mode {'enabled' if activate else 'disabled'}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to change Low Power Mode: {e}")


    @staticmethod
    def reduce_motion(activate: bool = True) -> None:
        if activate:
            subprocess.run(
                ["shortcuts", "run", "Motion-off"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Reduce Motion enabled")
        else:
            subprocess.run(
                ["shortcuts", "run", "Motion-on"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Reduce Motion disabled")


    @staticmethod
    def reduce_transparency(activate: bool = True) -> None:
        if activate:
            subprocess.run(
                ["shortcuts", "run", "Transparency-off"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Reduce Transparency enabled")
        else:
            subprocess.run(
                ["shortcuts", "run", "Transparency-on"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Reduce Transparency disabled")


    @staticmethod
    def set_wallpaper(file_name: str) -> None:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        WALLPAPER_PATH = os.path.join(BASE_DIR, "wallpapers", file_name)
        try:
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'tell application "System Events" to set picture of every desktop to "{WALLPAPER_PATH}"'
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            subprocess.run(["killall", "Dock"], check=True)
            print(f"✅ Wallpaper was changed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Wallpaper wasn't changed: {e}")


    @staticmethod
    def set_volume(volume: int) -> None:
        try:
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f"set volume output volume {volume}"
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Volume was changed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Volume wasn't changed: {e}")



