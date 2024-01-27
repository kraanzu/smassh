from pathlib import Path
from typing import List
from .parser import Parser
import appdirs

DEFAULTS = {
    "difficulty": "normal",
    "blind_mode": False,
    "min_speed": 0,
    "min_accuracy": 0,
    "min_burst": 0,
    "force_correct": False,
    "confidence_mode": "off",
    "capitalization_mode": "off",
    "cursor_buddy_speed": 0,
    "tab_reset": False,
    "language": "english",
    "numbers": False,
    "punctuations": False,
    "mode": "words",
    "words_count": 30,
    "time_count": 30,
    "caret_style": "block",
    "writing mode": "words",
    "theme": "nord",
}


class ConfigParser(Parser):
    """
    Inherited from `Parser` class to manage config
    """

    _root_dir = Path(__file__).parent.parent.parent
    config_path = Path(appdirs.user_config_dir("smassh"))
    DEFAULT_CONFIG = DEFAULTS

    @property
    def configured_languages(self) -> List[str]:
        from smassh.src.parser.data_parser import DataParser

        words_dir = DataParser.lang_path

        languages = [
            file_obj.stem
            for file_obj in words_dir.iterdir()
            if file_obj.suffix == ".json"
        ]
        return languages

    @property
    def configured_themes(self) -> List[str]:
        themes_dir = self._root_dir / "ui" / "css" / "themes"
        themes = [
            file_obj.stem
            for file_obj in themes_dir.iterdir()
            if file_obj.suffix == ".tcss"
        ]
        return themes

    def toggle_numbers(self) -> None:
        numbers = self.get("numbers")
        self.set("numbers", not numbers)

    def toggle_punctuations(self) -> None:
        punctuations = self.get("punctuations")
        self.set("punctuations", not punctuations)

    def toggle_mode(self) -> None:
        mode = self.get("mode")
        mode = "words" if mode == "time" else "time"
        self.set("mode", mode)

    @property
    def theme(self) -> str:
        return self.get("theme") or "nord"

    @theme.setter
    def theme(self, theme: str) -> None:
        self.set("theme", theme)


config_parser = ConfigParser()
