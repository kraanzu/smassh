from rich.console import RenderableType
from textual.app import ComposeResult, events
from textual.widget import Widget
from termtyper.ui.widgets.base_scroll import BaseWindow
from termtyper.ui.widgets.config_strip import TypingConfigStrip
from termtyper.ui.widgets.space import Space
from termtyper.ui.widgets.ticker import Ticker


class Pad(Widget):
    DEFAULT_CSS = """
    Pad.cspan3 {
        column-span: 3;
    }
    """

    def render(self) -> RenderableType:
        return ""


class TypingSpace(Widget):
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
    """

    def config_strip(self) -> ComposeResult:
        yield TypingConfigStrip()

    def counter(self) -> ComposeResult:
        yield Pad()
        yield Ticker("0")
        yield Pad()

    def space(self) -> ComposeResult:
        yield Pad()
        yield Space()
        yield Pad()

    def compose(self) -> ComposeResult:
        yield from self.config_strip()
        yield Pad(classes="cspan3")
        yield from self.counter()
        yield from self.space()

    def keypress(self, key: str):
        self.query_one(Space).keypress(key)


class TypingScreen(BaseWindow):
    def compose(self) -> ComposeResult:
        yield TypingSpace()

    def on_key(self, event: events.Key):
        key = event.key
        self.query_one(TypingSpace).keypress(key)
