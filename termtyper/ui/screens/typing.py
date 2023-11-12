from textual.app import ComposeResult
from termtyper.ui.widgets.base_scroll import BaseScroll
from termtyper.ui.widgets.config_strip import TypingConfigStrip


class TypingScreen(BaseScroll):

    DEFAULT_CSS = """
    TypingScreen {
        overflow: hidden;
    }
    """

    def compose(self) -> ComposeResult:
        yield TypingConfigStrip()
