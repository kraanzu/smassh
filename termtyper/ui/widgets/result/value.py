from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Digits, Label, Static


class ValueLabel(Label):
    pass


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
        self.wpm.update(str(stats.wpm))
        self.accuracy.update(str(stats.accuracy))

    def compose(self) -> ComposeResult:
        with AutoVertical():
            yield ValueLabel("WPM")
            yield self.wpm

        with AutoVertical():
            yield ValueLabel("ACC")
            yield self.accuracy
