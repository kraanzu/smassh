from textual.app import ComposeResult
from textual.screen import Screen
from termtyper.ui.screens.base import BaseScreen

from termtyper.ui.widgets.header import Header


class TypingScreen(BaseScreen):
    """
    The screen which shows the main typing screen
    """

    def compose(self) -> ComposeResult:
        yield Header()