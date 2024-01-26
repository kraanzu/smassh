from rich.console import RenderableType
from textual.app import ComposeResult, events
from textual.widget import Widget
from smassh.ui.widgets import (
    BaseWindow,
    TypingConfigStrip,
    PaletteOptions,
    Space,
    Ticker,
)
from textual.containers import VerticalScroll
from smassh.ui.events import SetScreen


class Pad(Widget):
    """
    Pad widget for empty spaces
    """

    DEFAULT_CSS = """
    Pad.cspan3 {
        column-span: 3;
    }
    """

    def render(self) -> RenderableType:
        return ""


class TypingSpace(Widget):
    """
    Widget that holds all the test paragraph and time ticker
    """

    DEFAULT_CSS = """
    TypingSpace {
        layout: grid;
        grid-size: 3 6;
        grid-columns: 1fr 4fr 1fr;
        grid-rows: 1 1fr 1 3 1fr 1;
        margin: 1;
        height: 100%;
        width: 100%;
    }

    VerticalScroll {
        scrollbar-size: 0 0;
    }

    """

    def config_strip(self) -> ComposeResult:
        yield TypingConfigStrip()

    def counter(self) -> ComposeResult:
        yield Pad()
        yield Ticker()
        yield Pad()

    def space(self) -> ComposeResult:
        yield Pad()
        with VerticalScroll():
            yield Space()
        yield Pad()

    def compose(self) -> ComposeResult:
        yield from self.config_strip()
        yield Pad(classes="cspan3")
        yield from self.counter()
        yield from self.space()
        yield Pad(classes="cspan3")
        yield PaletteOptions()

    def keypress(self, key: str):
        if key == "ctrl+s":
            return self.screen.post_message(SetScreen("settings"))

        if key == "ctrl+l":
            return self.app.push_screen("language")

        if key == "ctrl+t":
            return self.app.push_screen("theme")

        self.query_one(Space).keypress(key)


class TypingScreen(BaseWindow):
    """
    Screen Widget for typing area!
    """

    def compose(self) -> ComposeResult:
        yield TypingSpace()

    async def handle_key(self, event: events.Key):
        event.stop()
        key = event.character if event.is_printable and event.character else event.key
        self.query_one(TypingSpace).keypress(key)
