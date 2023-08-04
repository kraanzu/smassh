from textual.app import ComposeResult
from textual.screen import Screen
from termtyper.ui.screens.base import BaseScreen

from termtyper.ui.widgets.header import Header


class HelpScreen(BaseScreen):
    """
    Screen to show the help menu
    """

    def compose(self) -> ComposeResult:
        yield Header()
