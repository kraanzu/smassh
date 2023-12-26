from textual.containers import Vertical
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from termtyper.ui.widgets import (
    PaletteList,
    PaletteInput,
    LanguagePaletteList,
    ThemePaletteList,
)


class PaletteMenu(Vertical):
    DEFAULT_CSS = """
    PaletteMenu {
        width: 60%;
        height: 50%;
        layout: grid;
        grid-size: 1 2;
        grid-rows: 1 1fr;
    }
    """


class PaletteScreen(Screen):
    DEFAULT_CSS = """
    PaletteScreen {
        layout: vertical;
        align: center middle;
    }
    """
    BINDINGS = [
        Binding("escape", "app.pop_screen"),
        Binding("down", "next_option"),
        Binding("up", "prev_option"),
    ]

    palette_list: PaletteList
    palette_icon: str

    def action_next_option(self):
        self.query_one(PaletteList).action_cursor_down()

    def action_prev_option(self):
        self.query_one(PaletteList).action_cursor_up()

    def compose(self) -> ComposeResult:
        with PaletteMenu():
            yield PaletteInput()
            yield self.palette_list


class LanguagePaletteScreen(PaletteScreen):
    palette_list = LanguagePaletteList()
    palette_icon = "  "


class ThemePaletteScreen(PaletteScreen):
    palette_list = ThemePaletteList()
    palette_icon = "  "
