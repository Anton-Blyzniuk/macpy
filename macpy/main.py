from macpy.controllers import DisplayController, NetworkController

display = DisplayController()
network = NetworkController()

network.activate_bluetooth(False)

display.set_brightness(
    brightness=50
)
