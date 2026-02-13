from applepy.controllers import DisplayController, NetworkController, AppController

display = DisplayController(
    "37D8832A-2D66-02CA-B9F7-8F30A301B230"
)

apps = AppController()

print(apps.running_apps)

