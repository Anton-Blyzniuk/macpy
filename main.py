import sys
from default_scripts.planing import planing_func
from default_scripts.planing_close import planing_close_func
from default_scripts.close_all_apps import close_all_apps_func

scripts = {
    "planing": planing_func,
    "planing_close": planing_close_func,
    "close_all_apps": close_all_apps_func,
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
        print("Unknown script:", script_name)
        print("Available scritps:", ", ".join(scripts.keys()))



if __name__ == "__main__":
    main()
