from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widgets import Label, Static
from termtyper.ui.events import SetScreen
from termtyper.ui.widgets import Space


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

    def on_click(self, _) -> None:
        self.screen.query_one(Space).reset()
        self.post_message(SetScreen("typing"))


class RepeatTest(ResultStripItem):
    icon = ""
    help = "Repeat test"

    def on_click(self, _) -> None:
        self.screen.query_one(Space).restart()
        self.post_message(SetScreen("typing"))


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
