from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from termtyper.ui.settings_options import menu
from termtyper.ui.widgets.base_scroll import BaseScroll


class SettingsWidget(BaseScroll):
    DEFAULT_CSS = """
    .xxx {background: red}
    """

    def compose(self) -> ComposeResult:
        for name, items in menu.items():
            yield Static(name, classes="xxx")
            for item in items:
                yield item
