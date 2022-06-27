from os import wait
from rich.align import Align

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from textual import events
from termtyper.events.events import ParaSizeChange
from termtyper.ui.widgets.menu import Menu


class SizeMenu(Menu):
    def __init__(self):
        options = ["teensy", "small", "big", "huge"]
        super().__init__(
            "size_menu",
            options,
            ParaSizeChange,
            draw_border=True,
            title="How much can your fingers handle?"
        )
