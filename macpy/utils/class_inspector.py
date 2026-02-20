import inspect


class Inspector:
    @staticmethod
    def get_class_constructor(class_obj) -> dict:
        for name, attr in class_obj.__dict__.items():
            if not callable(attr):
                continue
            if name == "__init__":
                return {
                    "name": name,
                    "parameters": [
                        {
                            "name": p.name,
                            "annotation": p.annotation,
                            "default": p.default,
                        }
                        for p in inspect.signature(
                            attr
                        ).parameters.values() if p.name != "self" and p.name != "kwargs"
                    ]
                }
        return {
            "message": "constructor wasn't found",
        }



    @staticmethod
    def get_class_methods(class_obj) -> list[dict]:
        methods = []
        for name, attr in class_obj.__dict__.items():
            if not callable(attr):
                continue
            if name.startswith("__") or name.endswith("__"):
                continue
            methods.append(
                {
                    "name": name,
                    "parameters": [
                        {
                            "name": p.name,
                            "annotation": p.annotation,
                            "default": p.default,
                        }
                        for p in inspect.signature(
                            attr
                        ).parameters.values() if p.name != "self" and p.name != "kwargs"
                    ]
                }
            )
        return methods