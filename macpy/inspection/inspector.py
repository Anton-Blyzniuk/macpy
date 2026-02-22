import inspect
from inspect import Parameter


class Inspector:
    @staticmethod
    def get_constructor(cls) -> dict | None:
        try:
            sig = inspect.signature(cls.__init__)
        except (TypeError, ValueError):
            return None

        params = []
        for p in sig.parameters.values():
            if p.name == "self":
                continue
            if p.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
                continue

            params.append(
                {
                    "name": p.name,
                    "annotation": None if p.annotation is inspect._empty else p.annotation,
                    "default": None if p.default is inspect._empty else p.default,
                }
            )

        return {"name": "__init__", "parameters": params}

    @staticmethod
    def get_methods(cls) -> list[dict]:
        methods = []

        for name, func in inspect.getmembers(cls, inspect.isfunction):
            if name.startswith("_"):
                continue

            sig = inspect.signature(func)
            params = []

            for p in sig.parameters.values():
                if p.name == "self":
                    continue
                if p.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
                    continue

                params.append(
                    {
                        "name": p.name,
                        "annotation": None if p.annotation is inspect._empty else p.annotation,
                        "default": None if p.default is inspect._empty else p.default,
                    }
                )

            methods.append(
                {
                    "name": name,
                    "parameters": params,
                }
            )

        return methods