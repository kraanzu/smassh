from pathlib import Path
from .parser import Parser
import appdirs


DEFAULT_NUMBER_VALUES = {
    i: {"low": 100000, "med": 0, "high": 0} for i in (15, 30, 60, 120)
}


DEFAULTS = {
    "words": DEFAULT_NUMBER_VALUES,
    "time": DEFAULT_NUMBER_VALUES,
}


class DataParser(Parser):
    config_path = Path(appdirs.user_data_dir("smassh"))
    DEFAULT_CONFIG = DEFAULTS

    def add_stats(self, stats):

        ...


data_parser = DataParser()
