from typing import List, Tuple
from rich.console import RenderableType
from rich.table import box
from rich.text import Text
from textual.widget import Widget
from textual.app import ComposeResult
from smassh.src.help_menu import SETTINGS_KEYBINDS, TYPING_KEYBINDS, GENERAL_KEYBINDS
from smassh.ui.widgets.base_window import BaseWindow


class Table(Widget):
    """
    Table widget to show keybindings
    """

    DEFAULT_CSS = """
    Table {
        height: auto;
        content-align: center middle;
        align: center middle;
        margin: 1 3;
    }
    """

    COMPONENT_CLASSES = {"--header", "--key", "--action"}

    def __init__(self, title: str, keys: List[Tuple[str, str]] = []) -> None:
        super().__init__()
        self.title = title
        self.keys = keys

    def render(self) -> RenderableType:
        from rich.table import Table

        table_header = self.get_component_rich_style("--header")
        table_key = self.get_component_rich_style("--key")
        table_action = self.get_component_rich_style("--action")

        table = Table(
            expand=True,
            show_header=False,
            padding=(0, 0),
            box=box.SIMPLE,
            title=Text(
                f" 󰌌 Keybinds for {self.title}",
                style=table_header,
                justify="left",
            ),
        )
        table.add_column(Text("Key"), style=table_key, ratio=1)
        table.add_column("", width=5)
        table.add_column(Text("Action"), style=table_action, ratio=4)
        for key, description in self.keys:
            table.add_row(key, "", description)

        return table


class HelpScreen(BaseWindow):
    """
    Help Screen to show help tables for various screens
    """

    def compose(self) -> ComposeResult:
        yield Table("General Stuff", GENERAL_KEYBINDS)
        yield Table("Typing Screen", TYPING_KEYBINDS)
        yield Table("Settings Screen", SETTINGS_KEYBINDS)
