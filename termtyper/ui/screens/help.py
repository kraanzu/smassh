from typing import List, Tuple
from rich.console import RenderableType
from rich.table import box
from rich.text import Text
from textual.widget import Widget
from textual.app import ComposeResult
from termtyper.src.help_menu import SETTINGS_KEYBINDS, TYPING_KEYBINDS
from termtyper.ui.widgets.base_scroll import BaseWindow


class Table(Widget):
    DEFAULT_CSS = """
    Table {
        height: auto;
        content-align: center middle;
        align: center middle;
        margin: 1;
    }
    """

    def __init__(self, title: str, keys: List[Tuple[str, str]] = []):
        super().__init__()
        self.title = title
        self.keys = keys

    def render(self) -> RenderableType:
        from rich.table import Table

        table = Table(
            show_header=False,
            padding=(0, 0),
            box=box.SIMPLE,
            title=Text(
                f"Keybinds for {self.title}",
                style="black on blue",
            ),
        )
        table.add_column(Text("Key", style="black on green"), style="magenta")
        table.add_column("", width=5)
        table.add_column(Text("Action", style="black on green"), style="yellow")
        for key, description in self.keys:
            table.add_row(key, "", description)

        return table


class HelpScreen(BaseWindow):
    def compose(self) -> ComposeResult:
        yield Table("Typing Screen", TYPING_KEYBINDS)
        yield Table("Settings Screen", SETTINGS_KEYBINDS)
