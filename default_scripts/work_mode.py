from controls.app import AppController
from default_scripts.close_all_apps import close_all_apps_func
from controls.system import SystemController


def work_mode_func() -> None:
    close_all_apps_func()

    app_controller = AppController()
    app_controller.open_applications([
        "Google chrome",
        "ChatGPT"
    ])

    system_controller = SystemController()
    system_controller.set_volume(50)

    system_controller.set_wallpaper("default.jpg")
    system_controller.wi_fi()
    system_controller.bluetooth()
    system_controller.reduce_transparency(False)
    system_controller.reduce_motion(False)
    system_controller.low_power_mode(False)
    system_controller.airdrop("ContactsOnly")


if __name__ == "__main__":
    work_mode_func()
