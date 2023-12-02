from pathlib import Path
from .parser import Parser
import appdirs

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
    "language": "english",
    "numbers": False,
    "punctuations": False,
    "caret_style": "block",
    "bar_theme": "minimal",
    "writing mode": "words",
    "paragraph_size": "teensy",
    "timeout": "15",
}


class ConfigParser(Parser):
    config_path = Path(appdirs.user_config_dir("smassh"))
    section = "config"
    DEFAULT_CONFIG = DEFAULTS

    def toggle_numbers(self):
        numbers = self.get("numbers")
        self.set("numbers", "True" if str(numbers) == "False" else "False")

    def toggle_punctuations(self):
        punctuations = self.get("punctuations")
        self.set(
            "punctuations",
            "True" if str(punctuations) == "False" else "False",
        )


config_parser = ConfigParser()
