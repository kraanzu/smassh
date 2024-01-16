from textual.app import ComposeResult
from textual.widgets import Label
from termtyper.src.stats_tracker import StatsTracker
from termtyper.ui.widgets import BaseWindow
from termtyper.ui.widgets.typing.space import Space


class ResultScreen(BaseWindow):
    """
    This screen will show the result of the typing test.
    E.g. Typing Chart, Accuracy, WPM etc.
    """

    DEFAULT_CSS = """
    ResultScreen {
        layout: horizontal;
        align: center middle;
    }
    """

    def on_show(self):
        self.app.query_one(Space).reset()

    def compose(self) -> ComposeResult:
        yield Label("Result Screen")

    def set_results(self, stats: StatsTracker):
        self.stats = stats
