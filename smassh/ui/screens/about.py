from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from smassh.ui.widgets import BaseWindow

DESCRIPTION = """
Smassh is a TUI based typing test application inspired by MonkeyType
-- A very popular online web-based typing application

All the other TUI based applications I found were not graphically appealing
and then I discovered textual which made it possible to create this application.

Smassh tries to be a full fledged typing test experience but not missing
out on looks and feel!

A lot of work is still left to be done and I'll be more than happy to accept
any ideas and contributions :D

Thanks for checking out this project!
"""

STAR = """
[@click=app.star]Star this project on GitHub![/]
"""

OUTRO = """
Made with ❤️  by kraanzu
"""


class Section(Widget):
    """
    Section Widget for each section of About Menu
    """

    DEFAULT_CSS = """
    Section {
        height: auto;
        content-align: center middle;
    }
    """

    def __init__(self, renderable: str) -> None:
        super().__init__()
        self.renderable = renderable

    def render(self) -> RenderableType:
        return Text.from_markup(self.renderable)


class AboutDescription(Section):
    def __init__(self) -> None:
        super().__init__(DESCRIPTION)


class Star(Section):
    def __init__(self) -> None:
        super().__init__(STAR)


class AboutOutro(Section):
    DEFAULT_CSS = """
    AboutOutro {
        content-align: center bottom;
        height: 100%;
    }
    """

    def __init__(self) -> None:
        super().__init__(OUTRO)


class AboutScreen(BaseWindow):
    """
    About screen to show info about the project
    """

    DEFAULT_CSS = """
    AboutScreen {
        layout: grid;
        grid-size: 1 3;
        grid-rows: auto auto 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield AboutDescription()
        yield Star()
        yield AboutOutro()
