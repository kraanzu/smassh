from json import load, dump
import os
from pathlib import Path
from typing import Any, Dict, Literal, Union

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


def combine_into(d: dict, to: dict) -> None:
    for k, v in d.items():
        if isinstance(v, dict):
            combine_into(v, to.setdefault(k, {}))
        else:
            to[k] = v


class Parser:
    """
    A sub class of ConfigParser class
    to parse the currenty set options in the settings menu
    """

    _file_name = "smassh"
    config_path: Path
    DEFAULT_CONFIG: Dict[str, Any]

    def __init__(self) -> None:
        super().__init__()
        self.config = self.DEFAULT_CONFIG
        if not Path.is_file(self.full_path):
            self._create_user_config()
        else:
            self.update(self.read_from_file())

    @property
    def file_name(self) -> str:
        return self._file_name + ".json"

    @property
    def full_path(self) -> Path:
        return self.config_path.joinpath(self.file_name)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save()

    def update(self, data: Dict[str, Any]) -> None:
        combine_into(data, self.config)

    def save(self) -> None:
        with open(self.full_path, "w") as fp:
            dump(self.config, fp)

    def _create_user_config(self) -> None:
        """
        Creates a new config
        """

        os.makedirs(self.config_path, exist_ok=True)
        self.save()

    def get(self, data: str) -> Any:
        return self.config.get(data)

    def read_from_file(self) -> Dict[str, Any]:
        with open(self.full_path, "r") as fp:
            return load(fp)