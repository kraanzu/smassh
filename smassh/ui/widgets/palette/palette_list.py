from functools import cache
from typing import List, Type
from textual.message import Message
from textual.widgets import OptionList
from smassh.src import config_parser


class PaletteOptionHighlighted(Message):
    """
    Highlight Event for Palette when option is changed
    """

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class ApplyLanguage(PaletteOptionHighlighted):
    pass


class ApplyTheme(PaletteOptionHighlighted):
    pass


class PaletteList(OptionList, can_focus=False):
    """
    List Widget to list all the available options
    """

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

    def _get_options(self) -> List[str]:
        raise NotImplementedError

    @cache
    def get_options(self) -> List[str]:
        options = self._get_options()
        return sorted([option.replace("_", " ") for option in options])

    def get_current(self) -> str:
        raise NotImplementedError

    def apply_filter(self, filter_text: str) -> None:

        def valid_option(option_text: str) -> bool:
            if not filter_text:
                return True

            return filter_text in option_text

        self.clear_options()
        self._filter = filter_text
        valid_options = filter(valid_option, self.get_options())
        self.add_options(valid_options)

    async def on_mount(self, _) -> None:
        self.apply_filter("")
        options = sorted(self._get_options())
        index = options.index(self.get_current())
        self.highlighted = index


class LanguagePaletteList(PaletteList):
    _highlight_event = ApplyLanguage

    def _get_options(self) -> List[str]:
        return config_parser.configured_languages

    def get_current(self) -> str:
        return config_parser.get("language")


class ThemePaletteList(PaletteList):
    _highlight_event = ApplyTheme

    def _get_options(self) -> List[str]:
        return config_parser.configured_themes

    def get_current(self) -> None:
        return config_parser.get("theme")
