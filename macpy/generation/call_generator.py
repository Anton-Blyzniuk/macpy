class CallGenerator:

    @staticmethod
    def generate_constructor_code(
            class_name: str,
            variable_name: str,
            inspected_constructor: dict | None,
            values: dict[str, object]
    ) -> str:
        if not inspected_constructor:
            return f"{variable_name} = {class_name}()"

        args = []
        for p in inspected_constructor.get('parameters', []):
            name = p['name']
            if name in values:
                args.append(f"{name}={values[name]!r}")
        return f"{variable_name} = {class_name}({', '.join(args)})"

    @staticmethod
    def generate_method_call_code(
            variable_name: str,
            inspected_method: dict,
            values: dict[str, object]
    ) -> str:
        args = []
        for p in inspected_method.get('parameters', []):
            name = p['name']
            if name in values:
                args.append(f"{name}={values[name]!r}")
        return f"{variable_name}({', '.join(args)})"
