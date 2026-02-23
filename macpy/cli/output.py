from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CLIOutput:
    @staticmethod
    def output_list(arg_list: list, title: str) -> None:
        table = Table(
            title=title,
            show_lines=True,
        )

        table.add_column("Index", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Type", style="magenta")

        for i, value in enumerate(arg_list):
            table.add_row(
                str(i),
                repr(value),
                type(value).__name__
            )

        console.print(table)

    @staticmethod
    def output_error(error: str) -> None:
        console.print(
            Panel(
                error,
                title="Error",
                title_align="left",
                style="red"
            )
        )

    @staticmethod
    def output_message(message: str, title: str = "Info") -> None:
        console.print(
            Panel(
                message,
                title=title,
                title_align="left",
                style="cyan"
            )
        )