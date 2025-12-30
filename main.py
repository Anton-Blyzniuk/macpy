import sys
from default_scripts.planing import planing_func
from default_scripts.planing_close import planing_close_func
from default_scripts.close_all_apps import close_all_apps_func
from default_scripts.work_mode import work_mode_func
from default_scripts.game_mode import game_mode_func
from default_scripts.low_battery_mode import low_battery_mode_func
from dependencies import default_dependencies_check

scripts = {
    "planing": planing_func,
    "planing_close": planing_close_func,
    "close_all_apps": close_all_apps_func,
    "work_mode": work_mode_func,
    "game_mode": game_mode_func,
    "dependencies": default_dependencies_check,
    "low_battery_mode": low_battery_mode_func
}

def main() -> None:

    try:
        script_name = sys.argv[1]
    except Exception:
        print("Script name wasn't detected.")
        return

    if script_name in scripts:
        scripts[script_name]()
    else:
        if script_name != "list":
            print("Unknown script:", script_name)
        print("Available scritps:", ", ".join(scripts.keys()))



if __name__ == "__main__":
    main()
