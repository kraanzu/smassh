from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Digits, Static

from termtyper.src.parser import data_parser


class ValueLabel(Widget):
    DEFAULT_CSS = """
    ValueLabel {
        height: auto;
        width: auto;
    }
    """

    best = False

    def __init__(self, text: str, **kwargs):
        self.text = text
        super().__init__(**kwargs)

    def set_best(self, is_best: bool):
        self.best = is_best
        self.refresh()

    def render(self) -> RenderableType:
        best_icon = "👑" if self.best else ""
        return self.text + best_icon


class AutoVertical(Widget):
    DEFAULT_CSS = """
    AutoVertical {
        layout: vertical;
        margin: 1;
        height: auto;
        width: auto;
    }
    """


class Value(Digits, Static):
    DEFAULT_CSS = """
    Value {
        margin: 0 2;
        content-align: right middle;
        height: auto;
        width: auto;
    }
    """


class ValueContainer(Static):
    DEFAULT_CSS = """
    ValueContainer {
        layout: horizontal;
        margin: 0 2;
        height: auto;
        width: 100%;
        align: center middle;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wpm = Value()
        self.accuracy = Value()

    def update_stats(self, stats):

        wpm_label = self.query_one("#wpm_label", expect_type=ValueLabel)
        wpm_label.set_best(data_parser.is_highest_wpm(stats.wpm))

        self.wpm.update(str(stats.wpm))
        self.accuracy.update(str(stats.accuracy))

    def compose(self) -> ComposeResult:
        with AutoVertical():
            yield ValueLabel("WPM", id="wpm_label")
            yield self.wpm

        with AutoVertical():
            yield ValueLabel("ACC", id="acc_label")
            yield self.accuracy
