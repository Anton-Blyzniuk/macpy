import os
import sys
import subprocess
from curses.ascii import isdigit

from macpy import controllers, settings


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
            file[7:-3]
            for file in os.listdir(self.script_dir)
            if file.endswith(".py") and file.startswith("script_")
        ]


    def if_script_already_exists(self, script_name: str) -> bool:
        return script_name in self.available_scripts


    def create_script(self, script_name: str) -> None:
        code = (
            f"# {script_name} script\n"
            "from macpy.controllers import *\n\n"
        )
        controllers_objects = [getattr(controllers, name)() for name in controllers.__all__]
        if self.if_script_already_exists(script_name):
            print(f"Script {script_name} already exists.")
            return
        while True:
            for i in range(len(controllers_objects)):
                print(f"{i}. {controllers_objects[i].__class__.__name__}")

            action = input("Choose a controller: ")
            if action == "stop":
                break
            if not isdigit(action):
                print("Please enter a valid number.")
                continue
            if not int(action) in range(0, len(controllers_objects)):
                print("Please enter a valid number.")
                continue

            code += controllers_objects[int(action)].code()

        file_path = os.path.join(self.script_dir, f"script_{script_name}.py")
        with open(file_path, "w") as f:
            f.write(code)
        print(f"Script was created successfully: {file_path}")


    def run_script(self, script_name: str) -> None:
        if not self.if_script_already_exists(script_name):
            print(f"Script {script_name} does not exist.")
            return
        script_path = os.path.join(self.script_dir, f"script_{script_name}.py")
        subprocess.run(
            [sys.executable, script_path],
            check=True
        )

    def edit_script(self, script_name: str) -> None:
        os.system(f"{settings.CODE_EDITOR_COMMAND} {os.path.join(self.script_dir, f"script_{script_name}.py")}")


    def delete_script(self, script_name: str) -> None:
        if not self.if_script_already_exists(script_name):
            print(f"Script {script_name} does not exist.")
            return
        os.remove(os.path.join(self.script_dir, f"script_{script_name}.py"))
        if self.if_script_already_exists(script_name):
            raise Exception(f"Script {script_name} was not deleted.")

