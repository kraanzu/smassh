from textual.app import ComposeResult
from termtyper.ui.widgets.settings_options import menu
from termtyper.ui.widgets.base_scroll import BaseWindow


class SettingsScreen(BaseWindow):
    def compose(self) -> ComposeResult:
        for item in menu:
            yield item
