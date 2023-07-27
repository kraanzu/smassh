import os
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path
from typing import Any, Literal, Union

NumberType = Union[int, float]
SIZES = ["teensy", "small", "big", "huge"]
TIMES = ["15", "30", "60", "120"]
SpeedType = Literal["low", "med", "high"]

DEFAULTS = {
    "difficulty": "normal",
    "blind_mode": "off",
    "min_speed": "0",
    "min_accuracy": "0",
    "min_burst": "0",
    "force_correct": "off",
    "confidence_mode": "off",
    "capitalization_mode": "off",
    "single_line_words": "off",
    "cursor_buddy": "0",
    "cursor_buddy_speed": "0",
    "tab_reset": "off",
    "restart_same": "off",
    "paragraph_size": "teensy",
    "timeout": "15",
    "language": "english",
}

PARAPHRASE = {
    "numbers": False,
    "punctuations": False,
}

SPEED_RECORDS_WORDS = {
    **{f"{size}_low": 100000 for size in SIZES},
    **{f"{size}_med": 0 for size in SIZES},
    **{f"{size}_high": 0 for size in SIZES},
}

SPEED_RECORDS_TIME = {
    **{f"{time}_low": 100000 for time in TIMES},
    **{f"{time}_med": 0 for time in TIMES},
    **{f"{time}_high": 0 for time in TIMES},
}

THEMING = {
    "caret_style": "block",
    "bar_theme": "minimal",
    "sound": "mech",
    "keypress_sound": "off",
}

MODE = {
    "writing mode": "words",
}

CONF_DICT = {
    "user": DEFAULTS,
    "theming": THEMING,
    "paragraph": PARAPHRASE,
    "mode": MODE,
    "speed records word": SPEED_RECORDS_WORDS,
    "speed records time": SPEED_RECORDS_TIME,
}


def get_config_location() -> Path:
    """
    Finds the config dir for the system
    $XDG_CONFIG_HOME > ~/.config > ~/
    """

    try:
        return Path.expanduser(Path(os.environ["XDG_CONFIG_HOME"]))
    except KeyError:
        home = Path.home()
        config_dir = os.path.join(home, ".config")
        if os.path.isdir(config_dir):
            return Path(config_dir)
        else:
            return home


class Parser(ConfigParser):
    """
    A sub class of ConfigParser class
    to parse the currenty set options in the settings menu
    """

    config_path = get_config_location() / "termtyper"
    file_path = config_path / "termtyper.ini"

    def __init__(self) -> None:
        super().__init__()
        if not self.read(self.file_path):
            self._create_user_config()
        else:
            if len(self.sections()) == 1:
                self.clear()
                self._create_user_config()

    def _create_user_config(self) -> None:
        """
        Creates a new config
        """

        if not self.config_path.is_dir():
            os.mkdir(self.config_path)

        print("No config found !\nCreating....")
        with open(self.file_path, "w"):
            pass

        self.read_dict(CONF_DICT)

        self._write_to_file()

    def _add_default_config(self, section: str, option: str) -> None:
        if section in CONF_DICT:
            if option in CONF_DICT[section]:
                self.set(section, option, str(CONF_DICT[section][option]))
            else:
                raise NoOptionError(option, section)
        else:
            raise NoSectionError(section)

    def get(self, section: str, option: str, **kwargs) -> str:
        """
        Override the get method to add the default value if data doesn't exist
        """
        try:
            return super().get(
                section,
                option,
                raw=kwargs.get("raw", True),
                vars=kwargs.get("vars", None),
            )
        except NoOptionError:
            self._add_default_config(section, option)
            return super().get(
                section,
                option,
                raw=kwargs.get("raw", True),
                vars=kwargs.get("vars", None),
            )

    def toggle_numbers(self):
        numbers = self.get("paragraph", "numbers")
        self.set("paragraph", "numbers", "True" if str(numbers) == "False" else "False")

    def toggle_punctuations(self):
        punctuations = self.get("paragraph", "punctuations")
        self.set(
            "paragraph",
            "punctuations",
            "True" if str(punctuations) == "False" else "False",
        )

    def set(self, section: str, option: str, value: str | None = None) -> None:
        super().set(section, option, value)
        self._write_to_file()

    def set_speed(self, speed: SpeedType, value: NumberType) -> None:
        mode = self.get("mode", "writing mode")

        if mode == "words":
            paragraph_size = self.get_data("paragraph_size")
            self.set("speed records word", f"{paragraph_size}_{speed}", str(value))
        else:
            timeout = int(self.get_data("timeout"))
            self.set("speed records time", f"{timeout}_{speed}", str(value))

    def get_speed(self, speed: SpeedType) -> float:
        mode = self.get("mode", "writing mode")

        if mode == "words":
            paragraph_size = self.get_data("paragraph_size")
            return float(self.get("speed records word", f"{paragraph_size}_{speed}"))
        else:
            timeout = int(self.get_data("timeout"))
            return float(self.get("speed records time", f"{timeout}_{speed}"))

    def get_theme(self, data: str):
        return self.get("theming", data)

    def set_theme(self, data: str, value: Any):
        return self.set("theming", data, str(value))

    def get_para_setting(self, data: str) -> bool:
        return eval(self.get("paragraph", data))

    def set_para_setting(self, data: str, value: Any):
        return self.set("paragraph", data, str(value))

    def _write_to_file(self) -> None:
        with open(self.file_path, "w") as fp:
            self.write(fp)

    def get_data(self, data: str) -> str:
        return self.get("user", data)


MAIN_PARSER = Parser()
