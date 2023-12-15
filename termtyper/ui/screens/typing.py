from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from termtyper.ui.widgets.base_scroll import BaseWindow
from termtyper.ui.widgets.config_strip import TypingConfigStrip
from termtyper.ui.widgets.space import Space


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

    def compose(self) -> ComposeResult:
        yield TypingConfigStrip()
        yield Pad(classes="cspan3")
        yield Pad()
        yield Static("23")
        yield Pad()
        yield Pad()
        yield Space()
        yield Pad()
        for i in range(13):
            yield Pad()


class TypingScreen(BaseWindow):
    def compose(self) -> ComposeResult:
        yield TypingSpace()
