from typing import Callable


class CLIInput:
    supported_argument_types = [str, int, float, bool]

    @classmethod
    def is_supported_argument_type(cls, argument_type: type):
        if argument_type not in cls.supported_argument_types:
            raise TypeError(f"Argument type {argument_type} is not supported.")

    @classmethod
    def input_argument(
            cls,
            arg_type: type,
            message: str = None,
            validator: Callable = None,
            exit_word: str = None,
    ) -> str | int | float | bool:
        cls.is_supported_argument_type(arg_type)

        argument = input(message if message else "")
        if exit_word:
            if argument == exit_word:
                return exit_word
        try:
            argument = arg_type(argument)
        except (TypeError, ValueError):
            raise TypeError(f"Could not convert {argument} to {arg_type}.")

        if validator:
            if not validator(argument):
                raise TypeError(f"Argument {argument} is not a valid.")

        return argument

    @classmethod
    def input_list(
            cls,
            arg_type: type,
            message: str = None,
            detailed_message: str = None,
            validator: Callable = None,
            detailed_validator: Callable = None,
            exit_word: str = "exit"
    ) -> list[str] | list[int] | list[float] | list[bool]:
        cls.is_supported_argument_type(arg_type)

        print(message)

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