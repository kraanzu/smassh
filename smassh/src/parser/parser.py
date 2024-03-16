from json import load, dump
from pathlib import Path
from typing import Any, Dict


def combine_into(d: dict, to: dict) -> None:
    for k, v in d.items():
        if isinstance(v, dict):
            combine_into(v, to.setdefault(k, {}))
        else:
            to[k] = v


class Parser:
    """
    The base class for ConfigParser and DataParser classes
    """

    _file_name: str = "smassh"
    config_path: Path
    DEFAULT_CONFIG: Dict[str, Any]

    def __init__(self) -> None:
        self.config = self.DEFAULT_CONFIG.copy()
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

    def reset(self):
        self.config = self.DEFAULT_CONFIG
        self.save()

    def _create_user_config(self) -> None:
        """
        Creates a new config
        """

        self.config_path.mkdir(parents=True, exist_ok=True)
        self.save()

    def get(self, data: str) -> Any:
        return self.config.get(data)

    def read_from_file(self) -> Dict[str, Any]:
        with open(self.full_path, "r") as fp:
            return load(fp)
