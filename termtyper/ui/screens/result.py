from textual.app import ComposeResult
from textual.widgets import Label
from termtyper.ui.widgets import BaseWindow


class ResultScreen(BaseWindow):
    """
    This screen will show the result of the typing test.
    E.g. Typing Chart, Accuracy, WPM etc.
    """

    def compose(self) -> ComposeResult:
        yield Label("Result Screen")