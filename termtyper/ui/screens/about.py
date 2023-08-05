import webbrowser
from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget

from termtyper.src.getting_started import INTRO, KEYBINDS_HEADER, KEYBINGS, OUTRO
from termtyper.ui.screens.base import BaseScreen
from termtyper.ui.widgets.header import Header


class HorizontalRule(Widget):
    DEFAULT_CSS = """
    HorizontalRule {
        height: 1;
        content-align: center middle;
    }
    """

    def render(self) -> RenderableType:
        size = int(0.6 * self.size.width)
        return "━" * size


class AboutScroll(Widget):
    DEFAULT_CSS = """
    AboutScroll {
        layout: vertical;
        overflow-y: scroll;
        scrollbar-size: 1 1;
    }
    """


class AboutWidget(Widget):
    DEFAULT_CSS = """
    AboutWidget {
        height: auto;
        content-align: center middle;
        link-hover-background: red;  
    }
    """

    def __init__(self, renderable: str):
        super().__init__()
        self.renderable = renderable

    def render(self) -> RenderableType:
        return Text.from_markup(self.renderable)

class AboutScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield Header()
        with AboutScroll():
            yield AboutWidget(INTRO)
            yield HorizontalRule()
            yield AboutWidget(KEYBINDS_HEADER)
            yield HorizontalRule()
            yield AboutWidget(KEYBINGS)
            yield HorizontalRule()
            yield AboutWidget(OUTRO)