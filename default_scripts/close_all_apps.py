from controls.app import AppController


def close_all_apps_func() -> None:
    app_controller = AppController()
    app_controller.close_every_application_except([
        "Finder",
        "Ghostty",
        "Aerospace",
        "AlDente",
        "System Events",
        "Dock",
        "NotificationCenter",
    ])

    app_controller.force_close_applications([
        "Steam",
        "Discord"
    ])


if __name__ == "__main__":
    close_all_apps()

