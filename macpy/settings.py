import os

# Path to settings file
SETTINGS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "macpy",
    "settings.py",
)

# Display controller settings
DISPLAY_ID = "37D8832A-2D66-02CA-B9F7-8F30A301B230"

# Examples: code, nvim, vim, nano
CODE_EDITOR_COMMAND = "nvim"