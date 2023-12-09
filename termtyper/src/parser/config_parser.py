from pathlib import Path
from .parser import Parser
import appdirs

DEFAULTS = {
    "difficulty": "normal",
    "blind_mode": False,
    "min_speed": 0,
    "min_accuracy": 0,
    "min_burst": 0,
    "force_correct": False,
    "confidence_mode": False,
    "capitalization_mode": False,
    "single_line_words": False,
    "cursor_buddy": 0,
    "cursor_buddy_speed": 0,
    "tab_reset": False,
    "restart_same": False,
    "language": "english",
    "numbers": False,
    "punctuations": False,
    "caret_style": "block",
    "writing mode": "words",
    "theme": "nord",
}


class ConfigParser(Parser):
    config_path = Path(appdirs.user_config_dir("smassh"))
    DEFAULT_CONFIG = DEFAULTS

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
    def theme(self, theme):
        self.set("theme", theme)


config_parser = ConfigParser()
