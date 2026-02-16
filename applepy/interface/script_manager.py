import os

from applepy.controllers import(
    AppController,
    DesktopController,
    AudioController,
    DisplayController,
    NetworkController,
    PowerController
)


class ScriptManager:
    _instance = None
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, scripts_dir: None|str = None) -> None:
        if scripts_dir is None:
            self.script_dir = os.path.join(self.base_dir, "scripts")
        else:
            self.script_dir = scripts_dir
        os.makedirs(self.script_dir, exist_ok=True)

    @property
    def available_scripts(self) -> list[str]:
        return [
            file[:-3]
            for file in os.listdir(self.script_dir)
            if file.endswith(".py")
               and (file.startswith("script_") or file.endswith("_script.py"))
        ]

    def if_script_already_exists(self, script_name: str) -> bool:
        return script_name in self.available_scripts

    def create_script(self, script_name: str) -> None:
        code = f"""
        # {script_name} script
        
        from applepy.controllers import *
        
        """

        controllers = [
            AppController(),
            DesktopController(),
            AudioController(),
            DisplayController("37D8832A-2D66-02CA-B9F7-8F30A301B230"),
            NetworkController,
            PowerController(),
        ]
        counter = 0
        while True:
            if input(f"Do you want to include {controllers[counter].__class__.__name__}?[y/N]: ").lower() == "y":
                code += controllers[counter].generate_python_code()
            if counter == len(controllers) - 1:
                break
            counter += 1
        print(code)


    def run_script(self, script_name: str) -> None:
        if not self.if_script_already_exists(script_name):
            raise Exception(f"Script {script_name} does not exist.")

        os.system(
            f"python3 {os.path.join(self.script_dir, script_name)}.py"
        )

    def delete_script(self, script_name: str) -> None:
        if not self.if_script_already_exists(script_name):
            raise Exception(f"Script {script_name} does not exist.")

        os.remove(os.path.join(self.script_dir, f"{script_name}.py"))

        if script_name in self.available_scripts:
            raise Exception(f"Script {script_name} was not deleted.")

