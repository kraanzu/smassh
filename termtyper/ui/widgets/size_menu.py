from os import wait
from rich.align import Align

from rich.console import RenderableType
from rich.text import Text
from rich.tree import Tree
from textual import events
from termtyper.events.events import ParaSizeChange
from termtyper.ui.widgets.menu import Menu


class SizeMenu(Menu):
    def __init__(self):
        options = ["teensy", "small", "big", "huge"]
        super().__init__("size_menu", options)

    async def key_press(self, event: events.Key):
        match event.key:
            case "j" | "down":
                self.select_next_option()
            case "k" | "up":
                self.select_prev_option()
            case "enter":
                await self.post_message(
                    ParaSizeChange(self, self.options[self.cursor]),
                )

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        for index, i in enumerate(self.options):
            label = Text(i.ljust(self._max_len))

            if index == self._cursor:
                label.stylize("b green")
                label = Text(">  ") + label
            else:
                label = Text("   ") + label

            tree.add(Align.center(label))

        return self.render_panel(tree)
