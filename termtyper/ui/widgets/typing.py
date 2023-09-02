from textual.app import ComposeResult
from termtyper.ui.widgets.base_scroll import BaseScroll


class TypingSpace(BaseScroll):
    def compose(self) -> ComposeResult:
        return super().compose()
