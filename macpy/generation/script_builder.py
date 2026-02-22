class ScriptBuilder:

    @staticmethod
    def build_script(
            script_name: str,
            controller_usage_units: list[str],
    ) -> str:
        return (
            f"# In this file you can see code for '{script_name}' script.\n\n"
            "from macpy.controllers import *\n\n\n"
            f"{'\n\n'.join(controller_usage_units)}"
        )

    @staticmethod
    def build_controller_usage_unit(
            constructor_code: str,
            method_calls: list[str],
            comment: str
    ) -> str:
        return (
            f"# {comment}\n"
            f"{constructor_code}\n\n"
            f"{'\n'.join(method_calls)}"
            "\n"
        )