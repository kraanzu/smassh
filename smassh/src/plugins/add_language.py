from rich import print
import requests
import appdirs
from typing import Optional
from pathlib import Path

LANGUAGE_PACK_DIR = Path(appdirs.user_data_dir("smassh")) / "languages"


class AddLanguage:
    """
    Plugin to add new languages to smassh
    """

    def __init__(self, silent: bool = False) -> None:
        self.silent = silent

    def log(self, message: str, color: str = "green") -> None:
        """Logs a message to the console"""
        if not self.silent:
            print(f"=>[bold {color}] {message}[/bold {color}]")

    def get_pack(self, name: str) -> Optional[str]:
        """Checks if a language pack exists. If found, it returns its contents otherwise it returns None"""

        uri = f"https://raw.githubusercontent.com/monkeytypegame/monkeytype/master/frontend/static/languages/{name}.json"
        req = requests.get(uri)

        return req.text if (req.status_code == 200) else None

    def add(self, name: str) -> None:
        """Downloads a new language for smassh"""

        if not LANGUAGE_PACK_DIR.exists():
            LANGUAGE_PACK_DIR.mkdir()

        self.log("Checking if language pack exists...")

        pack = self.get_pack(name)

        if pack is None:
            return self.log("Language pack doesnt exist!", "red")

        LANGUAGE_FILE = LANGUAGE_PACK_DIR / f"{name}.json"

        if LANGUAGE_FILE.exists():
            return self.log("Language pack already exists", "green")

        self.log("Downloading language pack...")

        with open(LANGUAGE_FILE, "w") as f:
            f.write(pack)

        self.log("Successfully downloaded the language pack!")
