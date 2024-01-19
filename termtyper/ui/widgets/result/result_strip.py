from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widgets import Label, Static


class ResultStripItem(Label):
    DEFAULT_CSS = """
    ResultStripItem {
        padding: 0 3;
    }
    """

    icon: str
    help: str

    def on_mount(self) -> None:
        self.tooltip = self.help

    def render(self) -> RenderableType:
        return self.icon


class NextTest(ResultStripItem):
    icon = ""
    help = "Next test"


class RepeatTest(ResultStripItem):
    icon = ""
    help = "Repeat test"


class ResultStrip(Static):
    DEFAULT_CSS = """
    ResultStrip {
        layout: horizontal;
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield NextTest()
        yield RepeatTest()
