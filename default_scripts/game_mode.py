import os
from controls.app import AppController
from default_scripts.close_all_apps import close_all_apps_func
from controls.system import SystemController


def game_mode_func() -> None:
    close_all_apps_func()

    app_controller = AppController()
    app_controller.open_applications([
        "Steam",
        "Discord"
    ])

    system_controller = SystemController()
    system_controller.set_volume(60)

    system_controller.set_wallpaper("black.png")
    system_controller.wi_fi()
    system_controller.bluetooth()
    system_controller.reduce_transparency(True)
    system_controller.reduce_motion(True)
    system_controller.low_power_mode(False)
    system_controller.airdrop("Off")


if __name__ == "__main__":
    work_mode_func()
