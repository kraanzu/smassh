from textual.app import ComposeResult
from textual.containers import VerticalScroll

from termtyper.ui.widgets.base_scroll import BaseScroll


class HelpWidget(BaseScroll):
    def compose(self) -> ComposeResult:
        return super().compose()
