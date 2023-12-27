from textual.widgets import OptionList
from rich.text import Text
from termtyper.src.parser import config_parser


class PaletteList(OptionList, can_focus=False):
    DEFAULT_CSS = """
    PaletteList {
        border: none;
    }
    """
    _filter: str = ""

    def get_options(self):
        raise NotImplementedError

    def apply_filter(self, text):
        self._filter = text
        self.clear_options()
        for option in self.get_options():
            text = Text(option)
            count = text.highlight_words([self._filter], "green")
            if count:
                self.add_option(text)

    async def on_mount(self, _):
        self.apply_filter("")


class LanguagePaletteList(PaletteList):
    def get_options(self):
        return config_parser.configured_languages


class ThemePaletteList(PaletteList):
    def get_options(self):
        return config_parser.configured_themes
