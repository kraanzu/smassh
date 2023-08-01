from textual.app import ComposeResult
from textual.screen import Screen

from termtyper.ui.widgets.header import Header


class AboutScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
