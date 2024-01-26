from textual.app import ComposeResult
from textual.widget import Widget
from .palette import Palette


class LanguagePalette(Palette):
    screen_name = "language"
    config_name = "language"
    icon = ""


class ThemePalette(Palette):
    screen_name = "theme"
    config_name = "theme"
    icon = ""


class PaletteOptions(Widget):
    """
    Typing Space Widget which shows current enable palette options
    """

    DEFAULT_CSS = """
    PaletteOptions {
        layout: horizontal;
        align: center middle;
        height: 1;
        column-span: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield LanguagePalette()
        yield ThemePalette()
