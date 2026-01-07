from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from rich.console import Console
from rich.panel import Panel

from controls.app import AppController
from default_scripts.close_all_apps import close_all_apps_func
from controls.system import SystemController
from controls.display import DisplayController

console = Console()


def work_mode_func() -> None:
    display_controller = DisplayController(
        "37D8832A-2D66-02CA-B9F7-8F30A301B230"
    )
    app_controller = AppController()
    system_controller = SystemController()

    steps = [
        ("[bold cyan]Calibrating brightness[/bold cyan]",
         lambda: display_controller.calibrate_brightness()),

        ("Closing all applications",
         close_all_apps_func),

        ("Opening work applications",
         lambda: app_controller.open_applications([
             "Google Chrome",
             "ChatGPT",
         ])),

        ("Setting system volume",
         lambda: system_controller.set_volume(50)),

        ("Setting wallpaper",
         lambda: system_controller.set_wallpaper("default.jpg")),

        ("Configuring system toggles",
         lambda: (
             system_controller.wi_fi(),
             system_controller.bluetooth(),
             system_controller.reduce_transparency(False),
             system_controller.reduce_motion(False),
             system_controller.low_power_mode(False),
         )),

        ("Setting refresh rate",
         lambda: display_controller.set_refresh_rate(120)),

        ("Setting resolution",
         lambda: display_controller.set_resolution(1728, 1117)),

        ("Focusing terminal",
         lambda: app_controller.focus_application("Ghostty")),

        ("Final brightness adjustment",
         lambda: display_controller.set_brightness(60, False)),
    ]

    console.print("\n💼 [bold]Enabling Work Mode[/bold]\n")

    with Progress(
        SpinnerColumn(style="bold green"),
        TextColumn("[bold]{task.description}"),
        BarColumn(bar_width=30, complete_style="green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Starting...", total=len(steps))

        for name, step in steps:
            progress.update(task, description=name)
            try:
                step()
                progress.advance(task)
                console.print(f"  [green]✔[/green] {name}")
            except Exception as e:
                progress.stop()
                console.print(
                    Panel.fit(
                        str(e),
                        title="[red]Work mode failed[/red]",
                        border_style="red",
                    )
                )
                raise

    console.print(
        Panel.fit(
            "[bold green]Work mode is ready 🚀[/bold green]",
            title="macpy",
            border_style="green",
        )
    )


if __name__ == "__main__":
    work_mode_func()
