from rich.console import RenderableType
from textual.app import ComposeResult, events
from textual.containers import VerticalScroll
from textual.widget import Widget

from smassh.ui.events import SetScreen
from smassh.ui.widgets import (
    BaseWindow,
    PaletteOptions,
    Space,
    Ticker,
    TypingConfigStrip,
)


class TypingScroll(VerticalScroll, can_focus=False):
    pass


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
        with TypingScroll():
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

    @staticmethod
    def keypresses_from_text(text: str) -> list[str]:
        return [character for character in text if character.isprintable()]

    def type_text(self, text: str) -> None:
        typing_space = self.query_one(TypingSpace)
        for key in self.keypresses_from_text(text):
            typing_space.keypress(key)

    async def handle_key(self, event: events.Key):
        if not self.visible:
            return

        event.stop()
        key = event.character if event.is_printable and event.character else event.key
        self.query_one(TypingSpace).keypress(key)

    async def handle_paste(self, event: events.Paste) -> None:
        if not self.visible:
            return

        event.stop()
        self.type_text(event.text)
