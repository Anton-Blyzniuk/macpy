from typing import get_origin, get_args
from macpy.utils import Inspector


class CodeGeneratorMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._constructor = Inspector.get_class_constructor(cls)
        cls._methods = Inspector.get_class_methods(cls)

    @staticmethod
    def action_confirm(question: str) -> bool:
        return input(f"{question}[y/N]: ").lower() == "y"

    @staticmethod
    def request_argument(arg_type: type, message: str = None) -> str | int | float | bool:
        if not arg_type in [int, float, str, bool]:
            raise TypeError(f"Argument type {arg_type} is not supported.")

        return arg_type(input(message if message else ""))

    @staticmethod
    def show_list(list_to_show: list[str|int|float]) -> None:
        print(list_to_show)

    @classmethod
    def reqeust_list(
            cls,
            args_type: type,
            message: str = None,
            stop_word: str = None,
            view_word: str = None,
            clear_word: str = None,
            edit_word: str = None,
    ) -> list[int] | list[float] | list[str]:

        stop_word = stop_word or "stop"
        view_word = view_word or "view"
        clear_word = clear_word or "clear"
        edit_word = edit_word or "edit"

        result = []
        while True:
            arg = input(
                f"{len(result) + 1}. {message}" if message else f"{len(result) + 1}. "
            )

            if arg == stop_word:
                if cls.action_confirm(f"Is it correct?\n{result}\n"):
                    break

            elif arg == view_word:
                cls.show_list(result)
                continue

            elif arg == clear_word:
                if cls.action_confirm(f"Are you sure you want to clear: \n{result}\n"):
                    result.clear()
                continue

            elif arg == edit_word:
                cls.show_list(result)
                index = cls.request_argument(int, message="Index: ")
                result[index] = cls.request_argument(args_type)
                continue

            result.append(args_type(arg))

        return result

    def generate_constructor_code(self) -> str:
        args = []

        params = self._constructor.get("parameters")

        if params:
            for p in params:
                name = p["name"]
                if hasattr(self, name):
                    value = getattr(self, name)
                    args.append(f"{name}={value!r}")

        return f"{self.__class__.__name__.lower()} = {self.__class__.__name__}({', '.join(args)})\n"

    def generate_code(self) -> str:
        result = (
            f"# {self.__class__.__name__} actions\n"
            f"{self.generate_constructor_code()}"
        )

        for method in self._methods:
            name = method["name"]

            if name.startswith("_") or name.endswith("_"):
                continue

            if not self.action_confirm(f"Do you want to include {name}?"):
                continue

            result += f"{self.__class__.__name__.lower()}.{name}("

            parameters = method["parameters"]
            for i in range(0, len(parameters)):
                p = parameters[i]

                result += f"{p['name']}="
                if p["annotation"] in [int, float, str, bool]:
                    print(f"{name} requires an argument {p['name']}: {p["annotation"]}: ")
                    result += f"{self.request_argument(p["annotation"], message=f"-> {p['name']}: ")}"

                elif get_origin(p["annotation"]) is list or p["annotation"] is list:
                    print(f"{name} requires a list {p['name']}: {p["annotation"]}: ")
                    result += f"{self.reqeust_list(get_args(p["annotation"])[0])}"

                if i + 1 != len(parameters):
                    result += ", "

            result += ")\n"

        return result

    def code(self):
        result = (
            f"# {self.__class__.__name__} actions\n"
            f"{self.generate_constructor_code()}"
        )

        while True:
            for i, method in enumerate(self._methods):
                print(f"{i}. {method['name']}")

            action = input("Select a method: ").strip()

            if action == "stop":
                break
            if not action.isdigit():
                print("Please enter a valid number.")
                continue

            index = int(action)
            if index not in range(len(self._methods)):
                print("Please enter a valid number.")
                continue

            method = self._methods[index]
            name = method["name"]

            result += f"{self.__class__.__name__.lower()}.{name}("

            parameters = method["parameters"]
            for i, p in enumerate(parameters):
                result += f"{p['name']}="

                if p["annotation"] in (int, float, str, bool):
                    print(f"{name} requires an argument {p['name']}: {p['annotation']}")
                    result += str(
                        self.request_argument(
                            p["annotation"],
                            message=f"-> {p['name']}: "
                        )
                    )

                elif get_origin(p["annotation"]) is list or p["annotation"] is list:
                    print(f"{name} requires a list {p['name']}: {p['annotation']}")
                    result += str(
                        self.request_list(get_args(p["annotation"])[0])
                    )

                if i + 1 != len(parameters):
                    result += ", "

            result += ")\n"

        return result


