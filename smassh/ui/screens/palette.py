from textual import on, work
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Label
from smassh.ui.widgets import (
    PaletteList,
    PaletteInput,
    LanguagePaletteList,
    ThemePaletteList,
)


class PaletteMenu(Vertical):
    """
    A menu to show all the avaialble options for the setting
    """

    DEFAULT_CSS = """
    PaletteMenu {
        width: 60%;
        height: 50%;
        layout: grid;
        grid-size: 1 3;
        grid-rows: 2 3 1fr;
    }
    """


class PaletteHeader(Label):
    """
    Header widget to show setting name of palette menu
    """

    DEFAULT_CSS = """
    PaletteHeader {
        content-align: center middle;
        width: 100%;
    }
    """


class PaletteScreen(Screen):
    """
    Screen for palette with dark mask over main window
    """

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
    @work(thread=True, exclusive=True)
    def update_palette_list(self, event: PaletteInput.Changed) -> None:
        """
        Function to filter changes based on Input field in Palette

        Args:
            event (PaletteInput.Changed): Change Event
        """

        event.stop()
        text = self.query_one(PaletteInput).value
        self.query_one(PaletteList).apply_filter(text)

    @on(PaletteList.OptionHighlighted)
    def preview_palette_option(self, event: PaletteList.OptionHighlighted) -> None:
        """
        Function to preview change in smassh

        Args:
            event (PaletteList.OptionHighlighted): Change Event
        """

        palette_list = self.query_one(PaletteList)
        prompt = str(event.option.prompt)
        prompt = prompt.replace(" ", "_")
        self.post_message(palette_list._highlight_event(prompt))

    def action_next_option(self) -> None:
        self.query_one(PaletteList).action_cursor_down()

    def action_prev_option(self) -> None:
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
