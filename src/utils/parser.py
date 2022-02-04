import os
from configparser import ConfigParser


class Parser(ConfigParser):
    file_path = os.path.join(os.path.expanduser("~"), ".termtyper.ini")

    def __init__(self) -> None:
        if not self.read(self.file_path):
            self._create_user_config()
            self.read(self.file_path)

    def _create_user_config(self) -> bool:
        raise NotImplemented

    def set(self, data: str, val: str):
        super().set("user", data, val)

    def get(self, data: str) -> str:
        return super().get("user", data)
