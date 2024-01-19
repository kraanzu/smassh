from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widgets import Label, Static


class ResultStripItem(Label):
    DEFAULT_CSS = """
    ResultStripItem {
        margin: 0 3;
    }
    """

    icon: str

    def render(self) -> RenderableType:
        return self.icon


class NextTest(ResultStripItem):
    icon = ""


class RepeatTest(ResultStripItem):
    icon = ""


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
