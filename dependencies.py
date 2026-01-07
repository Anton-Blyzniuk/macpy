import subprocess
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TaskProgressColumn,
)
from rich.console import Console


console = Console()

def render_progress(current: int, total: int, width: int = 30) -> None:
    percent = int((current / total) * 100)
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\rProgress: [{bar}] {percent}% ({current}/{total})", end="", flush=True)

def log(msg: str) -> None:
    print(f"\n{msg}", flush=True)

def is_brew_installed() -> None:
    try:
        subprocess.run(
            ["brew", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"❌ Brew is not instelled.\nInstall it here: https://brew.sh/")


def is_dependencies_installed(dependencies: list[dict]) -> None:
    for d in dependencies:
        t = d.get("type")
        n = d.get("name")
        try:
            subprocess.run(
                ["brew", "list", f"--{t}", n],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"❌ {n} is not installed.\nInstall it with this command: brew install --{t} {n}")


def is_shortcuts_available(shortcuts: list[dict]) -> None:
    result = subprocess.run(
        ["shortcuts", "list"],
        capture_output=True,
        text=True,
        check=True
    )
    existing = result.stdout.splitlines()

    for s in shortcuts:
        name = s.get("name")
        desc = s.get("description")

        if name in existing:
            pass
        else:
            raise Exception(
                f"❌ {name} is not available.\n"
                f"Create it in the Shortcuts app with this name: {name}\n"
                f"Description: {desc}"
            )

def default_dependencies_check() -> None:
    steps = [
        ("[bold cyan]Homebrew[/bold cyan]", is_brew_installed()),
        ("displayplacer", lambda: is_dependencies_installed([
            {"type": "formula", "name": "displayplacer"}
        ])),
        ("blueutil", lambda: is_dependencies_installed([
            {"type": "formula", "name": "blueutil"}
        ])),
        ("cloudflare-warp", lambda: is_dependencies_installed([
            {"type": "cask", "name": "cloudflare-warp"}
        ])),
        ("Shortcuts", lambda: is_shortcuts_available([
            {"name": "Motion-on", "description": "Turns on motion"},
            {"name": "Motion-off", "description": "Turns off motion"},
            {"name": "Transparency-off", "description": "Turns off transparency"},
            {"name": "Transparency-on", "description": "Turns on transparency"},
        ])),
    ]

    console.print("\n[bold]🔍 Checking system dependencies[/bold]\n")

    with Progress(
        SpinnerColumn(style="bold green"),
        TextColumn("[bold]{task.description}"),
        BarColumn(bar_width=30, complete_style="green"),
        TaskProgressColumn(),  # %
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Starting...", total=len(steps))

        for name, step in steps:
            progress.update(task, description=name)
            step()
            progress.advance(task)

    console.print("\n[bold green]✅ Ready to operate[/bold green]\n")


if __name__ == "__main__":
    default_dependencies_check()

