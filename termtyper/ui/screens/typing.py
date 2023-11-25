from textual.app import ComposeResult
from termtyper.ui.widgets.base_scroll import BaseWindow
from termtyper.ui.widgets.config_strip import TypingConfigStrip
from termtyper.ui.widgets.space import Space


class TypingScreen(BaseWindow):
    def compose(self) -> ComposeResult:
        yield TypingConfigStrip()
        yield Space()
