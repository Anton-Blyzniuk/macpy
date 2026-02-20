import sys
from macpy.scripts import ScriptManager


def main():
    script_manager = ScriptManager()

    try:
        action = sys.argv[1]
    except IndexError:
        raise Exception("You must specify an action.")

    if action == "run":
        try:
            script_name = sys.argv[2]
        except IndexError:
            raise Exception("You must specify a script.")

        script_manager.run_script(script_name)

    if action == "list":
        print(script_manager.available_scripts)

    if action == "delete":
        try:
            script_name = sys.argv[2]
        except IndexError:
            raise Exception("You must specify a script.")

        script_manager.delete_script(script_name)

    if action == "create":
        try:
            script_name = sys.argv[2]
        except IndexError:
            raise Exception("You must specify a name.")

        script_manager.create_script(script_name)

    if action == "edit":
        try:
            script_name = sys.argv[2]
        except IndexError:
            raise Exception("You must specify a script.")

        script_manager.edit_script(script_name)







if __name__ == "__main__":
    main()