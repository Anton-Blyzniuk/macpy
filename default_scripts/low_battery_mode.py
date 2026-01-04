from default_scripts.close_all_apps import close_all_apps_func
from controls.system import SystemController
from controls.custom import cloudflare_warp_connection
from controls.display import DisplayController


def low_battery_mode_func() -> None:
    display_conroller = DisplayController("37D8832A-2D66-02CA-B9F7-8F30A301B230")
    display_conroller.calibrate_brightness()

    close_all_apps_func()

    system_controller = SystemController()

    system_controller.set_volume(0)
    system_controller.set_wallpaper("black.png")
    system_controller.wi_fi(False)
    system_controller.bluetooth(False)
    system_controller.reduce_transparency(True)
    system_controller.reduce_motion(True)
    system_controller.low_power_mode(True)


    print(
        display_conroller.set_refresh_rate(47)["message"]
    )
    print(
        display_conroller.set_resolution(1168, 755)["message"]
    )
    print(
        display_conroller.set_brightness(10, False)["message"]
    )
    cloudflare_warp_connection(False)


def test_func() -> None:
    print("test_func is empty")

if __name__ == "__main__":
    low_battery_mode_func()
