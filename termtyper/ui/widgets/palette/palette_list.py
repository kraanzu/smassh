from typing import Type
from textual.message import Message
from textual.widgets import OptionList
from rich.text import Text
from termtyper.src.parser import config_parser


class PaletteOptionHighlighted(Message):
    def __init__(self, value: str):
        super().__init__()
        self.value = value


class ApplyLanguage(PaletteOptionHighlighted):
    pass


class ApplyTheme(PaletteOptionHighlighted):
    pass


class PaletteList(OptionList, can_focus=False):
    DEFAULT_CSS = """
    PaletteList {
        border: none;
        scrollbar-size: 0 1;

        .option-list--option {
            padding: 0 1;
        }

    }
    """

    _filter: str = ""
    _highlight_event: Type[PaletteOptionHighlighted]

    def get_options(self):
        raise NotImplementedError

    def apply_filter(self, text):
        self._filter = text
        self.clear_options()
        for option in self.get_options():
            option = option.replace("_", " ")
            text = Text(option)
            count = text.highlight_words([self._filter], "green")
            if count:
                self.add_option(text)

    async def on_mount(self, _):
        self.apply_filter("")


class LanguagePaletteList(PaletteList):
    _highlight_event = ApplyLanguage

    def get_options(self):
        return config_parser.configured_languages


class ThemePaletteList(PaletteList):
    _highlight_event = ApplyTheme

    def get_options(self):
        return config_parser.configured_themes
