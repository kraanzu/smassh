from smassh.src.parser import config_parser
from .option import BaseOption, Confirm


class ResetConfig(Confirm):
    def __init__(self) -> None:

        def callback():
            config_parser.reset()
            for setting in self.screen.query(BaseOption):
                setting.load_current_setting()
                setting.refresh()

        super().__init__("rest_config", "Reset", callback)
