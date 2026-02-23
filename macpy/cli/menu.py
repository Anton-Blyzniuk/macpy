from macpy.cli import CLIInput, CLIOutput
from typing import get_origin, get_args
from typing import Any
from macpy import controllers, generation, inspection
from rich.console import Console

console = Console()


class CLIMenu:

    @staticmethod
    def show_list_and_select_element(
            list_element: list,
            message: str,
            exit_word: str,
            title: str,
            confirm_action: bool = False,
    ) -> Any:
        console.clear()
        CLIOutput.output_list(list_element, title=title)
        while True:
            result = CLIInput.input_argument(
                arg_type=int,
                message=message,
                exit_word=exit_word,
            )
            if result == exit_word:
                return exit_word
            if confirm_action:
                if not CLIInput.confirm_action("Are you sure?"):
                    continue
            if result not in range(0, len(list_element)):
                CLIOutput.output_error(
                    error="Element doesn't exist.",
                )
                continue
            return result



    @staticmethod
    def get_method_values(method) -> dict:
        values = {}
        for p in method.get("parameters", []):
            annotation = p.get("annotation")
            if annotation in [int, float, str]:
                values[p.get("name")] = CLIInput.input_argument(
                    arg_type=annotation,
                    message=f"'{method.get('name')}' requires {p.get('name')}[{annotation}]"
                )
            elif annotation is bool:
                CLIOutput.output_message(
                    message=f"'{method.get('name')}' requires {p.get('name')}[boolean]"
                )
                values[p.get("name")] = CLIInput.input_boolean(
                    message=f"'{method.get('name')}' requires {p.get('name')}[True/False]"
                )
            elif get_origin(annotation) is list:
                CLIOutput.output_message(
                    message=f"'{method.get('name')}' requires list {p.get('name')}[{get_args(annotation)[0]}]\n"
                            f"type 'exit' to exit",
                )
                values[p.get("name")] = CLIInput.input_list(
                    arg_type=get_args(annotation)[0],
                )
        return values

    @staticmethod
    def get_method_calls(methods) -> list[str]:
        result = []
        for method in methods:
            result.append(
                generation.CallGenerator.generate_method_call_code(
                    inspected_method=method,
                    variable_name=controllers.AppController.__name__.lower(),
                    values=CLIMenu.get_method_values(
                        method
                    ),
                )
            )
        return result

    @staticmethod
    def get_controller_usage_unit(controller_class) -> str:
        method_calls = []
        inspected_methods = inspection.Inspector.get_methods(controller_class)
        method_names = [method.get("name") for method in inspected_methods]
        while True:
            choice = CLIMenu.show_list_and_select_element(
                list_element=method_names,
                message=f"Enter method index",
                exit_word="exit",
                confirm_action=False,
                title="Methods",
            )
            if choice == "exit":
                break
            method = inspected_methods[choice]
            method_calls.append(
                generation.CallGenerator.generate_method_call_code(
                    inspected_method=method,
                    variable_name=controller_class.__name__.lower(),
                    values=CLIMenu.get_method_values(
                        method=method
                    )
                )
            )

        return generation.ScriptBuilder.build_controller_usage_unit(
            generation.CallGenerator.generate_constructor_code(
                inspected_constructor=inspection.Inspector.get_constructor(controller_class),
                class_name=controller_class.__name__,
                variable_name=controller_class.__name__.lower(),
                values=CLIMenu.get_method_values(
                    method=inspection.Inspector.get_constructor(controller_class)
                )
            ),
            method_calls=method_calls,
            comment=f"{controller_class.__name__} usage unit:"
        )


if __name__ == "__main__":
    print(CLIMenu.get_controller_usage_unit(controller_class=controllers.DisplayController))


