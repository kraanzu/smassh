import os
from configparser import ConfigParser
from typing import Literal, Union

NumberType = Union[int, float]
SIZES = ["teensy", "small", "big", "huge"]
SpeedType = Literal["low", "med", "high"]

DEFAULTS = {
    "difficulty": "normal",
    "blind_mode": "off",
    "min_speed": "0",
    "min_accuracy": "0",
    "min_burst": "0",
    "force_correct": "off",
    "confidence_mode": "off",
    "single_line_words": "off",
    "caret_style": "block",
    "cursor_buddy": "0",
    "cursor_buddy_speed": "0",
    "tab_reset": "off",
    "restart_same": "off",
    "keypress_sound": "off",
    "paragraph_size": "teensy",
    "bar_theme": "minimal",
    "sound": "mech",
    **{f"{size}_low": "100000" for size in SIZES},
    **{f"{size}_med": "0" for size in SIZES},
    **{f"{size}_high": "0" for size in SIZES},
}


def get_config_location() -> str:
    """
    Finds the config dir for the system
    $XDG_CONFIG_HOME > ~/.config > ~/
    """

    try:
        return os.environ["XDG_CONFIG_HOME"]
    except KeyError:
        home = os.path.expanduser("~")
        config_dir = os.path.join(home, ".config")
        if os.path.isdir(config_dir):
            return config_dir
        else:
            return home


class Parser(ConfigParser):
    """
    A sub class of ConfigParser class
    to parse the currenty set options in the settings menu
    """

    config_path = os.path.join(get_config_location(), "termtyper")
    file_path = os.path.join(config_path, "termtyper.ini")

    def __init__(self) -> None:
        super().__init__()
        if not self.read(self.file_path):
            self._create_user_config()
            self.read(self.file_path)

    def _create_user_config(self) -> None:
        """
        Creates a new config
        """

        try:
            os.mkdir(self.config_path)
        except FileExistsError:
            pass

        print("No config found !\nCreating....")

        with open(self.file_path, "w"):
            pass

        self.add_section("user")

        # FOR SETTINGS
        for i, j in DEFAULTS.items():
            self.set_data(i, j)

        self._write_to_file()

    def set_speed(
        self, speed: Literal["low", "med", "high"], value: NumberType
    ) -> None:
        paragraph_size = self.get_data("paragraph_size")
        self.set_data(f"{paragraph_size}_{speed}", str(value))

    def get_speed(self, speed: SpeedType) -> float:
        paragraph_size = self.get_data("paragraph_size")
        return float(self.get_data(f"{paragraph_size}_{speed}"))

    def _write_to_file(self) -> None:
        with open(self.file_path, "w") as fp:
            self.write(fp)

    def set_data(self, data: str, val: str) -> None:
        super().set("user", data, val)
        self._write_to_file()

    def get_data(self, data: str) -> str:
        try:
            return super().get("user", data)
        except:
            default = DEFAULTS[data]
            self.set_data(data, default)
            return default
