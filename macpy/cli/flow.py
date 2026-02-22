from macpy.cli import CLIMenu
from macpy import controllers, generation


class CLIInterface:
    @staticmethod
    def create_script_flow(script_name: str) -> str:
        usage_units = []
        controllers_names = [c.__name__ for c in controllers.__available_controllers__]
        while True:
            choice = CLIMenu.show_list_and_select_element(
                list_element=controllers_names,
                message=f"Select controller: ",
                exit_word="exit",
                confirm_action=True,
            )
            if choice == "exit":
                break

            usage_units.append(
                CLIMenu.get_controller_usage_unit(
                    controllers.__available_controllers__[choice],
                )
            )

        return generation.ScriptBuilder.build_script(
            script_name=script_name,
            controller_usage_units=usage_units,
        )

if __name__ == "__main__":
    print(CLIInterface.create_script_flow("new_script"))