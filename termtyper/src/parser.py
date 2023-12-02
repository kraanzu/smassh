import os
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Literal, Union

NumberType = Union[int, float]
SpeedType = Literal["low", "med", "high"]
SIZES = ["teensy", "small", "big", "huge"]
TIMES = ["15", "30", "60", "120"]

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

DATA_DICT = {
    "speed records word": SPEED_RECORDS_WORDS,
    "speed records time": SPEED_RECORDS_TIME,
}


class Parser(ConfigParser):
    """
    A sub class of ConfigParser class
    to parse the currenty set options in the settings menu
    """

    _file_name = "smassh"
    _section: str
    config_path: Path
    DEFAULT_CONFIG: Dict[str, Dict[str, str]]

    def __init__(self) -> None:
        super().__init__()
        if not self.read(self.full_path):
            self._create_user_config()

    @property
    def file_name(self) -> str:
        return self._file_name + ".yaml"

    @property
    def full_path(self) -> Path:
        return self.config_path.joinpath(self._file_name)

    def save(self) -> None:
        with open(self.full_path, "w") as fp:
            self.write(fp)

    def _create_user_config(self) -> None:
        """
        Creates a new config
        """

        os.makedirs(self.config_path, exist_ok=True)
        self.read_dict(self.DEFAULT_CONFIG)
        self.save()

    def _add_default_config(self, section: str, option: str) -> None:
        self.set(section, option, str(self.DEFAULT_CONFIG[section][option]))

    def set(self, section: str, option: str, value: str | None = None) -> None:
        super().set(section, option, value)
        self.save()

    def get_data(self, data: str) -> str:
        return self.get(self._section, data)

    # def set_speed(self, speed: SpeedType, value: NumberType) -> None:
    #     mode = self.get("mode", "writing mode")
    #
    #     if mode == "words":
    #         paragraph_size = self.get_data("paragraph_size")
    #         self.set("speed records word", f"{paragraph_size}_{speed}", str(value))
    #     else:
    #         timeout = int(self.get_data("timeout"))
    #         self.set("speed records time", f"{timeout}_{speed}", str(value))
    #
    # def get_speed(self, speed: SpeedType) -> float:
    #     mode = self.get("mode", "writing mode")
    #
    #     if mode == "words":
    #         paragraph_size = self.get_data("paragraph_size")
    #         return float(self.get("speed records word", f"{paragraph_size}_{speed}"))
    #     else:
    #         timeout = int(self.get_data("timeout"))
    #         return float(self.get("speed records time", f"{timeout}_{speed}"))
