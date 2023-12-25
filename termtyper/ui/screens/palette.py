from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from termtyper.ui.widgets.palette_menu import (
    PaletteMenu,
    LanguagePaletteMenu,
    ThemePaletteMenu,
)


class PaletteScreen(Screen):
    DEFAULT_CSS = """
    PaletteScreen {
        layout: vertical;
        align: center middle;
    }
    """
    BINDINGS = [
        Binding("escape", "app.pop_screen"),
    ]

    palette_widget: PaletteMenu

    def compose(self) -> ComposeResult:
        yield self.palette_widget


class LanguagePaletteScreen(PaletteScreen):
    palette_widget = LanguagePaletteMenu()


class ThemePaletteScreen(PaletteScreen):
    palette_widget = ThemePaletteMenu()
