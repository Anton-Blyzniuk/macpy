from controls.app import AppController
from default_scripts.close_all_apps import close_all_apps_func
from controls.system import SystemController
from controls.display import DisplayController


def work_mode_func() -> None:

    display_conroller = DisplayController("37D8832A-2D66-02CA-B9F7-8F30A301B230")
    display_conroller.calibrate_brightness()

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

    display_conroller = DisplayController("37D8832A-2D66-02CA-B9F7-8F30A301B230")
    print(
        display_conroller.set_refresh_rate(120)["message"]
    )
    print(
        display_conroller.set_resolution(1728, 1117)["message"]
    )
    app_controller.focus_application("Ghostty")
    print(
        display_conroller.set_brightness(60, False)["message"]
    )


if __name__ == "__main__":
    work_mode_func()
