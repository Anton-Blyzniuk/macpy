from controls.app import AppController
from default_scripts.close_all_apps import close_all_apps_func
from controls.system import SystemController
from controls.display import DisplayController


def game_mode_func() -> None:
    display_conroller = DisplayController("37D8832A-2D66-02CA-B9F7-8F30A301B230")
    display_conroller.calibrate_brightness()

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

    print(
        display_conroller.set_refresh_rate(120)["message"]
    )
    print(
        display_conroller.set_resolution(1168, 755)["message"]
    )
    app_controller.focus_application("Ghostty")
    print(
        display_conroller.set_brightness(70, False)["message"]
    )


if __name__ == "__main__":
    game_mode_func()
