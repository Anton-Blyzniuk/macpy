from macpy.cli import CLIInput
from typing import Any

class CLIMenu:

    @staticmethod
    def show_list(arg_list: list) -> None:
        for i in range(len(arg_list)):
            print(f"[Index: {i}] -> ({arg_list[i]} : {type(arg_list[i]).__name__})")

    @staticmethod
    def show_error(error: Exception, message: str) -> None:
        print(f"{message} -> {error}")

    @staticmethod
    def select_element_from_list(arg_list: list, message: str, exit_word: str) -> Any:
        return arg_list[
            CLIInput.input_argument(
                arg_type=int,
                message=message,
                validator=lambda value: value in range(len(arg_list)),
                exit_word=exit_word
            )
        ]

    @staticmethod
    def confirm_action(question: str) -> bool:
        return CLIInput.input_argument(
            arg_type=str,
            message=question,
        ).lower() == "y"

