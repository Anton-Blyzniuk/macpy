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
            return {
                "status": True,
                "message": f"✅ Wi-Fi {'enabled' if activate else 'disabled'}"
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Wi-Fi state wasn't changed"
            }


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
            return {
                "status": True,
                "message": f"✅ Bluetooth {'enabled' if activate else 'disabled'}"
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Bluetooth state wasn't changed"
            }


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
            return {
                "status": True,
                "message": f"✅ Low Power Mode {'enabled' if activate else 'disabled'}"
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Low Power Mode wasn't changed"
            }


    @staticmethod
    def reduce_motion(activate: bool = True) -> None:
        if activate:
            subprocess.run(
                ["shortcuts", "run", "Motion-off"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {
                "status": True,
                "message": f"✅ Reduce Motion enabled"
            }
        else:
            subprocess.run(
                ["shortcuts", "run", "Motion-on"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {
                "status": True,
                "message": f"✅ Reduce Motion disabled"
            }


    @staticmethod
    def reduce_transparency(activate: bool = True) -> None:
        if activate:
            subprocess.run(
                ["shortcuts", "run", "Transparency-off"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {
                "status": True,
                "message": f"✅ Reduce Transparency enabled"
            }
        else:
            subprocess.run(
                ["shortcuts", "run", "Transparency-on"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {
                "status": True,
                "message": f"✅ Reduce Transparency disabled"
            }


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
            return {
                "status": True,
                "message": f"✅ Wallpaper was set to {file_name}"
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Wallpaper wasn't set to {file_name}"
            }


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
            return {
                "status": True,
                "message": f"✅ Volume was set to {volume}%"
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": False,
                "message": f"❌ Volume wasn't set to {volume}%"
            }



