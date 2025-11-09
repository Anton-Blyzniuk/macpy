import subprocess


def is_brew_installed() -> None:
    try:
        subprocess.run(
            ["brew", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"✅ Brew is installed.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"❌ Brew is not instelled.\nInstall it here: https://brew.sh/")


def is_dependencies_installed(dependencies: list[dict]) -> None:
    for d in dependencies:
        t = d.get("type")
        n = d.get("name")
        try:
            subprocess.run(
                ["brew", "list", f"--{t}", n],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ {n} is installed.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"❌ {n} is not installed.\nInstall it with this command: brew install --{t} {n}")


def default_dependencies_check() -> None:
    is_brew_installed()
    is_dependencies_installed(
        [
            {
                "type": "formula",
                "name": "displayplacer"
            },
            {
                "type": "formula",
                "name": "blueutil"
            },
            {
                "type": "cask",
                "name": "cloudflare-warp"
            },
        ]
    )


if __name__ == "__main__":
    default_dependencies_check()

