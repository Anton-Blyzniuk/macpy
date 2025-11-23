from controls.app import AppController


def planing_close_func() -> None:
    app_controller = AppController()
    app_controller.close_applications(["Reminders", "Calendar"])


if __name__ == "__main__":
    planing_close_func()
