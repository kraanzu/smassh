from pathlib import Path
from .parser import Parser
import appdirs

DEFAULTS = {}


class DataParser(Parser):
    config_path = Path(appdirs.user_data_dir("smassh"))
    DEFAULT_CONFIG = DEFAULTS


data_parser = DataParser()
