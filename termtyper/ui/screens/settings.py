from textual.app import ComposeResult
from termtyper.ui.widgets.settings_options import menu
from termtyper.ui.widgets.base_scroll import BaseScroll


class SettingsWidget(BaseScroll):
    def compose(self) -> ComposeResult:
        for item in menu:
            yield item
