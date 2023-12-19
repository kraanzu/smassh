from textual import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget

from termtyper.ui.widgets.palette import Palette


class LanguagePalette(Palette):
    @property
    def current_language(self) -> str:
        return "english"

    def render(self) -> RenderableType:
        return f" {self.current_language}"


class ThemePalette(Palette):
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
