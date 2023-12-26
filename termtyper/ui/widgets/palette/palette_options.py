from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget

from .palette import Palette


class LanguagePalette(Palette):
    screen_name = "language"

    @property
    def current_language(self) -> str:
        return "english"

    def render(self) -> RenderableType:
        return f" {self.current_language}"


class ThemePalette(Palette):
    screen_name = "theme"

    @property
    def current_theme(self) -> str:
        return "nord"

    def render(self) -> RenderableType:
        return f" {self.current_theme}"


class PaletteOptions(Widget):
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
