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
    "capitalization_mode": False,
    "single_line_words": False,
    "cursor_buddy": 0,
    "cursor_buddy_speed": 0,
    "tab_reset": False,
    "restart_same": False,
    "language": "english",
    "numbers": False,
    "punctuations": False,
    "mode": "words",
    "word_count": 30,
    "time_count": 30,
    "caret_style": "block",
    "writing mode": "words",
    "theme": "nord",
}


class ConfigParser(Parser):
    _root_dir = Path(__file__).parent.parent.parent
    config_path = Path(appdirs.user_config_dir("smassh"))
    DEFAULT_CONFIG = DEFAULTS

    @property
    def configured_languages(self) -> List[str]:
        words_dir = self._root_dir / "assets" / "words"
        languages = [
            file_obj.stem
            for file_obj in words_dir.iterdir()
            if file_obj.stem != "__init__"
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

    def toggle_numbers(self):
        numbers = self.get("numbers")
        self.set("numbers", not numbers)

    def toggle_punctuations(self):
        punctuations = self.get("punctuations")
        self.set("punctuations", not punctuations)

    @property
    def theme(self):
        return self.get("theme") or "nord"

    @theme.setter
    def theme(self, theme: str):
        self.set("theme", theme)


config_parser = ConfigParser()
