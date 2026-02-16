import inspect
from types import FunctionType
from typing import get_origin, get_args


class CLIMixin:
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

    @classmethod
    def reflection(cls) -> list[dict]:
        methods_info = []
        for name, attr in cls.__dict__.items():
            if not callable(attr):
                continue

            method_type = "instance"
            if isinstance(attr, staticmethod):
                method_type = "staticmethod"
                func = attr.__func__
            elif isinstance(attr, classmethod):
                method_type = "classmethod"
                func = attr.__func__
            elif isinstance(attr, FunctionType):
                func = attr
            else:
                continue

            signature = inspect.signature(func)

            methods_info.append({
                "name": name,
                "type": method_type,
                "signature": str(signature),
                "return_annotation": signature.return_annotation,
                "parameters": [
                    {
                        "name": p.name,
                        "annotation": p.annotation,
                        "default": p.default,
                        "kind": p.kind,
                    }
                    for p in signature.parameters.values() if p.name != "self" and p.name != "kwargs"
                ],
            })

        return methods_info


    @classmethod
    def generate_python_code(cls):
        reflection = cls.reflection()

        result = (
            f"# {cls.__name__} actions\n"
            f"{cls.__name__.lower()} = {cls.__name__}"
            f"()\n\n"
        )
        for method in reflection:
            name = method["name"]

            if name.startswith("_") or name.endswith("_"):
                continue

            if not cls.action_confirm(f"Do you want to include {name}?"):
                continue

            result += f"{cls.__name__.lower()}.{name}("

            parameters = method["parameters"]
            for i in range(0, len(parameters)):
                p = parameters[i]

                result += f"{p['name']}="
                if p["annotation"] in [int, float, str, bool]:
                    print(f"{name} requires an argument {p['name']}: {p["annotation"]}: ")
                    result += f"{cls.request_argument(p["annotation"], message=f"-> {p['name']}: ")}"

                elif get_origin(p["annotation"]) is list or p["annotation"] is list:
                    print(f"{name} requires a list {p['name']}: {p["annotation"]}: ")
                    result += f"{cls.reqeust_list(get_args(p["annotation"])[0])}"

                if i + 1 != len(parameters):
                    result += ", "

            result += ")\n"

        return result
