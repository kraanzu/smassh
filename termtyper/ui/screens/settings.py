from textual.app import ComposeResult
from textual.screen import Screen

from termtyper.ui.widgets.header import Header


class SettingsScreen(Screen):
    """
    Screen to show the settings
    """

    def compose(self) -> ComposeResult:
        yield Header()
