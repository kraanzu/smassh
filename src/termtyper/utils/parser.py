import os
from configparser import ConfigParser
import subprocess
from pathlib import Path


class Parser(ConfigParser):
    """
    A class to parse the currenty set options in the settings menu
    """

    file_path = os.path.join(os.path.expanduser("~"), ".termtyper.ini")

    def __init__(self) -> None:
        super().__init__()
        if not self.read(self.file_path):
            with open(self.file_path, "w"):
                pass

            self._create_user_config()
            self.read(self.file_path)

    def set_sound_location(self):
        loc = [
            i[10:]
            for i in subprocess.check_output("pip show rich".split())
            .decode()
            .splitlines()
            if i.startswith("Location")
        ][0]
        loc = Path().joinpath(loc, "termtyper", "sounds")
        self.set_data("sounds_loc", str(loc))

    def _create_user_config(self):

        self.add_section("user")

        # FOR SETTINGS
        self.set_data("difficulty", "normal")
        self.set_data("blind_mode", "off")
        self.set_data("min_speed", "0")
        self.set_data("min_accuracy", "0")
        self.set_data("min_burst", "0")
        self.set_data("force_correct", "off")
        self.set_data("confidence_mode", "off")
        self.set_data("single_line_words", "off")
        self.set_data("caret_style", "block")
        self.set_data("cursor_buddy", "0")
        self.set_data("cursor_buddy_speed", "0")
        self.set_data("tab_reset", "off")
        self.set_data("restart_same", "off")
        self.set_data("keypress_sound", "off")
        self.set_data("paragraph_size", "teensy")
        self.set_data("sound", "mech")

        # FOR MAINTING THE SPEED RECORDS
        self.set_data("low", "100000")
        self.set_data("med", "0")
        self.set_data("high", "0")

        # Sounds location
        self.set_sound_location()

        self._write_to_file()

    def _write_to_file(self):
        with open(self.file_path, "w") as fp:
            self.write(fp)

    def set_data(self, data: str, val: str):
        super().set("user", data, val)
        self._write_to_file()

    def get_data(self, data: str) -> str:
        return super().get("user", data)
