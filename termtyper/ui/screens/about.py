from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from termtyper.ui.widgets.base_scroll import BaseScroll


class HorizontalRule(Widget):
    DEFAULT_CSS = """
    HorizontalRule {
        height: 1;
        content-align: center middle;
    }
    """

    def render(self) -> RenderableType:
        size = int(0.6 * self.size.width)
        return "━" * size


class Section(Widget):
    DEFAULT_CSS = """
    Section {
        height: auto;
        content-align: center middle;
        link-hover-background: red;
    }
    """

    def __init__(self, renderable: str):
        super().__init__()
        self.renderable = renderable

    def render(self) -> RenderableType:
        return Text.from_markup(self.renderable)


class AboutDescription(Section):
    def __init__(self):
        TEXT = """\
    Termtyper is a TUI typing application which was highly inspired
    by monkeytype -- An online web-based typing application which is
    by far the most customizable typing application

    Termtyper tries to bring features of monkeytype to terminal
    """
        super().__init__(TEXT)
        self.styles.padding = 2


class Sponsor(Section):
    def __init__(self):
        TEXT = """\
    [@click=app.sponsor]Sponsor this project on GitHub![/],
    """
        super().__init__(TEXT)


class AboutOutro(Section):
    def __init__(self):
        TEXT = """\
        Made with ❤️  by kraanzu
        """
        super().__init__(TEXT)


class AboutScreen(BaseScroll):
    def compose(self) -> ComposeResult:
        yield AboutDescription()
        yield Sponsor()
        yield AboutOutro()
