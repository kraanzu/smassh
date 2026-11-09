from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

from smassh.src import data_parser
from smassh.src.stats_tracker import Match, StatsTracker
from smassh.ui.widgets import BaseWindow
from smassh.ui.widgets.line_chart import LineChart
from smassh.ui.widgets.result import ResultStrip, Value, ValueContainer
from smassh.ui.widgets.typing.space import Space
from smassh.ui.widgets.typing.ticker import Ticker


class AutoVertical(Static):
    DEFAULT_CSS = """
    AutoVertical {
        margin: 1;
        height: auto;
        width: auto;
        background: red;
    }
    """


class AutoHorizontal(Static):
    DEFAULT_CSS = """
    AutoVertical {
        layout: horizontal;
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
        layout: grid;
        grid-size: 1 6;
        grid-rows: 1fr auto auto 12 1 1fr;
        align: center middle;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.wpm = Value()
        self.accuracy = Value()

    def compose(self) -> ComposeResult:
        yield Container()
        yield ValueContainer()
        yield Static(id="history-comparison", markup=False)
        yield LineChart("Speed during this test (WPM)", id="attempt-speed")
        yield ResultStrip()
        yield Container()

    def set_results(self, stats: StatsTracker) -> None:
        summary = data_parser.summary()
        text = f"Raw {stats.raw_wpm} WPM · Accuracy {stats.accuracy}% · {stats.elapsed_time:.1f}s · Errors {stats.incorrect} · Missed {stats.missed}"
        if summary["count"]:
            difference = stats.wpm - summary["average_wpm"]
            text += f"\nPrevious {summary['count']} comparable tests: average {summary['average_wpm']:.1f} WPM · Best {summary['best_wpm']} · Change {difference:+.1f} WPM"
        else:
            text += "\nFirst result for these settings. Ctrl+G opens progress."
        self.query_one("#history-comparison", Static).update(text)
        samples = []
        words = 0
        correct = 0
        incorrect = 0
        for checkpoint in stats.checkpoints:
            words += checkpoint.letter == " "
            correct += checkpoint.correct == Match.MATCH
            incorrect += checkpoint.correct == Match.MISMATCH
            if checkpoint.elapsed > 0 and correct + incorrect:
                samples.append(
                    (
                        checkpoint.elapsed,
                        words
                        * 60
                        / checkpoint.elapsed
                        * correct
                        / (correct + incorrect),
                    )
                )
        duration = stats.elapsed_time
        labels = ("0s", f"{duration / 2:.0f}s", f"{duration:.0f}s")
        self.query_one("#attempt-speed", LineChart).set_series(samples, labels)
        self.stats = stats
        self.query_one(ValueContainer).update_stats(stats)

    def on_hide(self) -> None:
        space = self.screen.query_one(Space)
        if space.paragraph.spans:
            self.screen.query_one(Ticker).reset()
            space.restart()
