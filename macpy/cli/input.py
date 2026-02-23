from typing import Callable
from rich.prompt import Confirm
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from typing import Any
from rich.text import Text


console = Console()

class CLIInput:
    supported_argument_types = [str, int, float]

    @classmethod
    def is_supported_argument_type(cls, argument_type: type):
        if argument_type not in cls.supported_argument_types:
            raise TypeError(f"Argument type {argument_type} is not supported.")

    @staticmethod
    def confirm_action(question: str) -> bool:
        return Confirm.ask(
            f"[bold yellow]{question}[/bold yellow]",
            default=False
        )

    @classmethod
    def input_argument(
            cls,
            arg_type: type,
            message: str | None = None,
            validator: Callable | None = None,
            exit_word: str | None = None,
    ) -> Any:
        cls.is_supported_argument_type(arg_type)

        while True:
            prompt_text = Text()

            if message:
                prompt_text.append("› ", style="bold cyan")
                prompt_text.append(message, style="bold white")

            argument = Prompt.ask(prompt_text, console=console)

            if exit_word and argument == exit_word:
                return exit_word

            try:
                argument = arg_type(argument)
            except (TypeError, ValueError):
                console.print(
                    Panel(
                        f"[red]Could not convert[/red] '{argument}' to {arg_type.__name__}",
                        border_style="red",
                    )
                )
                continue

            if validator and not validator(argument):
                console.print(
                    Panel(
                        f"[yellow]Invalid value:[/yellow] {argument}",
                        border_style="yellow",
                    )
                )
                continue

            return argument

    @staticmethod
    def input_boolean(
            message: str = None,
            exit_word: str = None,
    ) -> bool | None:
        argument = str(input(message if message else "")).lower()
        if argument == exit_word:
            return exit_word
        if argument in ("yes", "y", "true"):
            return True
        return False

    @classmethod
    def input_list(
            cls,
            arg_type: type,
            message: str = None,
            detailed_message: str = None,
            validator: Callable = None,
            detailed_validator: Callable = None,
            exit_word: str = "exit"
    ) -> list[str] | list[int] | list[float]:
        cls.is_supported_argument_type(arg_type)

        result = []
        while True:
            arg = cls.input_argument(
                arg_type=arg_type,
                message=f"{len(result) + 1}. {detailed_message}" if detailed_message else f"{len(result) + 1}. ",
                validator=detailed_validator,
                exit_word=exit_word,
            )

            if arg == exit_word:
                if validator:
                    if validator(result):
                        return result
                    else:
                        raise ValueError("Generated list is not a valid.")
                return result

            result.append(arg)


if __name__ == "__main__":
    print(CLIInput.input_list(
        arg_type=int,
        message="You will have to enter numbers: ",
        detailed_message="number: ",
        validator=lambda numbers: len(numbers) > 0,
        detailed_validator=lambda number: number > 0,
        exit_word="exit",
    ))