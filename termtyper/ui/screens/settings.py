from textual.app import ComposeResult
from termtyper.ui.screens.base import BaseScreen

from termtyper.ui.widgets.header import Header


class SettingsScreen(BaseScreen):
    """
    Screen to show the settings
    """

    def compose(self) -> ComposeResult:
        yield Header()
