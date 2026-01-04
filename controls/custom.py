import subprocess


def cloudflare_warp_connection(activate: bool = True) -> None:
    try:
        state = "connect" if activate else "disconnect"
        subprocess.run(
            ["warp-cli", state],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return {
            "status": True,
            "message": f"✅ Cloudflare warp connection {'enabled' if activate else 'disabled'}"
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": False,
            "message": f"❌ Cloudflare warp connection state wasn't changed"
        }


# Here you can add your custom controllers.

if __name__ == "__main__":
    cloudflare_warp_connection(False)

