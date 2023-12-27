from textual import on
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Label
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
        grid-size: 1 3;
        grid-rows: 1 3 1fr;
    }
    """


class PaletteHeader(Label):
    DEFAULT_CSS = """
    PaletteHeader {
        content-align: center middle;
        width: 100%;
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
    palette_header: str

    @on(PaletteInput.Changed)
    def update_palette_list(self, event):
        event.stop()
        text = self.query_one(PaletteInput).value
        self.query_one(PaletteList).apply_filter(text)

    @on(PaletteList.OptionHighlighted)
    def preview_palette_option(self, event: PaletteList.OptionHighlighted):
        palette_list = self.query_one(PaletteList)
        prompt = str(event.option.prompt)
        self.post_message(palette_list._highlight_event(prompt))

    def action_next_option(self):
        self.query_one(PaletteList).action_cursor_down()

    def action_prev_option(self):
        self.query_one(PaletteList).action_cursor_up()

    def compose(self) -> ComposeResult:
        with PaletteMenu():
            yield PaletteHeader(self.palette_header)
            yield PaletteInput()
            yield self.palette_list


class LanguagePaletteScreen(PaletteScreen):
    palette_list = LanguagePaletteList()
    palette_icon = "  "
    palette_header = f"{palette_icon} language"


class ThemePaletteScreen(PaletteScreen):
    palette_list = ThemePaletteList()
    palette_icon = "  "
    palette_header = f"{palette_icon} themes"
