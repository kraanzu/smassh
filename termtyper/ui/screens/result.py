from textual.app import ComposeResult
from textual.widgets import Digits, Label, Static
from termtyper.src.stats_tracker import StatsTracker
from termtyper.ui.widgets import BaseWindow
from termtyper.ui.widgets.typing.space import Space


class ValueLabel(Label):
    pass


class Value(Digits, Static):
    DEFAULT_CSS = """
    Value {
        margin: 0 2;
        content-align: right middle;
        height: auto;
        width: auto;
    }
    """


class AutoVertical(Static):
    DEFAULT_CSS = """
    AutoVertical {
        margin: 1;
        height: auto;
        width: auto;
    }
    """


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wpm = Value()
        self.accuracy = Value()

    def compose(self) -> ComposeResult:
        with AutoVertical():
            yield ValueLabel("WPM")
            yield self.wpm

        with AutoVertical():
            yield ValueLabel("ACC")
            yield self.accuracy

    def on_show(self):
        self.app.query_one(Space).reset()

    def set_results(self, stats: StatsTracker):
        self.stats = stats
        self.wpm.update(str(stats.wpm))
        self.accuracy.update(str(stats.accuracy))
