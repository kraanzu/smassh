from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Digits, Static

from smassh.src.parser import data_parser


class ValueLabel(Widget):
    """
    Label Widgets for values in result screen
    """

    DEFAULT_CSS = """
    ValueLabel {
        height: auto;
        width: auto;
    }
    """

    COMPONENT_CLASSES = {"--personal-best"}

    best = False

    def __init__(self, text: str, **kwargs) -> None:
        self.text = Text(text)
        super().__init__(**kwargs)

    def set_best(self, is_best: bool) -> None:
        self.best = is_best
        self.refresh()

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("--personal-best")
        best_icon = Text(" 󱟜 " if self.best else "", style=style)
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
    """
    Widget to show result values in larger font size
    """

    DEFAULT_CSS = """
    Value {
        margin: 0 2;
        content-align: right middle;
        height: auto;
        width: auto;
    }
    """


class ValueContainer(Static):
    """
    Container widget that holds all the Values
    """

    DEFAULT_CSS = """
    ValueContainer {
        layout: horizontal;
        margin: 0 2;
        height: auto;
        width: 100%;
        align: center middle;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.wpm = Value()
        self.accuracy = Value()

    def update_stats(self, stats) -> None:
        wpm_label = self.query_one("#wpm_label", expect_type=ValueLabel)
        wpm_label.set_best(data_parser.is_highest_wpm(stats.wpm))

        acc_label = self.query_one("#acc_label", expect_type=ValueLabel)
        acc_label.set_best(data_parser.is_highest_accuracy(stats.accuracy))

        self.wpm.update(str(stats.wpm))
        self.accuracy.update(str(stats.accuracy))

    def compose(self) -> ComposeResult:
        with AutoVertical():
            yield ValueLabel("WPM", id="wpm_label")
            yield self.wpm

        with AutoVertical():
            yield ValueLabel("ACC", id="acc_label")
            yield self.accuracy
