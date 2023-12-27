from textual.widgets import OptionList
from termtyper.src.parser import config_parser


class PaletteList(OptionList, can_focus=False):
    DEFAULT_CSS = """
    PaletteList {
        border: none;
    }
    """

    def get_options(self):
        raise NotImplementedError

    async def on_mount(self, _):
        self.add_options(self.get_options())


class LanguagePaletteList(PaletteList):
    def get_options(self):
        return config_parser.configured_languages


class ThemePaletteList(PaletteList):
    def get_options(self):
        return config_parser.configured_themes
