from textual.app import ComposeResult
from textual.screen import Screen

from termtyper.ui.widgets.header import Header


class HelpScreen(Screen):
    """
    Screen to show the help menu
    """

    def compose(self) -> ComposeResult:
        yield Header()
