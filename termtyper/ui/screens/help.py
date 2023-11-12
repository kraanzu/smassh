from textual.app import ComposeResult
from termtyper.src.help_menu import HELP_MESSAGE

from termtyper.ui.widgets.base_scroll import BaseScroll


class HelpWidget(BaseScroll):
    def compose(self) -> ComposeResult:
        yield HELP_MESSAGE
