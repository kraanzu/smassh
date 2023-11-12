from textual.app import ComposeResult
from termtyper.ui.widgets.base_scroll import BaseScroll


class TypingScreen(BaseScroll):
    def compose(self) -> ComposeResult:
        return super().compose()
