from controls.app import AppController

def planing_func() -> None:
    app_controller = AppController()
    app_controller.open_applications([
        "Reminders",
        "Calendar"
    ])

if __name__ == "__main__":
    planing_func()
