from typing import Any
from macpy.cli import CLIMenu


class CLIInterface:
    @staticmethod
    def show_list_and_select_element(
            list_element: list,
            message: str,
            exit_word: str,
            confirm_action: bool = False
    ) -> Any:
        while True:
            CLIMenu.show_list(list_element)
            try:
                result = CLIMenu.select_element_from_list(
                    message=message,
                    arg_list=list_element,
                    exit_word=exit_word
                )
                if confirm_action:
                    if not CLIMenu.confirm_action("Are you sure? [y/N]: "):
                        continue
                return result
            except ValueError as error:
                CLIMenu.show_error(error=error, message="Element not found.")
