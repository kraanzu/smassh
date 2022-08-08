from rich.align import Align
from rich.console import RenderableType
from rich.text import Text
from rich.tree import Tree
from termtyper.events.events import (
    BarThemeChange,
    ModeChange,
    ParaSizeChange,
    TimeoutChange,
)
from termtyper.ui.widgets.menu import Menu


class SizeMenu(Menu):
    def __init__(self):
        options = ["teensy", "small", "big", "huge"]
        super().__init__(
            "paragraph_size",
            options,
            ParaSizeChange,
            draw_border=True,
            title="How much words can your fingers handle?",
            section="user",
            live_change=False,
        )


class TimeoutMenu(Menu):
    def __init__(self):
        options = ["15", "30", "60", "120"]
        super().__init__(
            "timeout",
            options,
            TimeoutChange,
            draw_border=True,
            title="How much time can your fingers last?",
            section="user",
            live_change=False,
        )

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        for index, i in enumerate(self.options):
            label = Text(i.ljust(self._max_len))
            label.append(" seconds")

            if index == self._cursor:
                label.stylize("b green")
                label = Text("> ") + label
            else:
                label = Text("  ") + label

            tree.add(Align.center(label))
        return self.render_panel(tree)


class BarThemeMenu(Menu):
    def __init__(self):
        options = ["minimal", "pacman", "doge", "balloon", "rust"]
        super().__init__(
            "bar_theme",
            options,
            BarThemeChange,
            draw_border=True,
            title="Choose your theme",
            section="theming",
        )


class ModeMenu(Menu):
    def __init__(self):
        options = ["words", "time"]
        super().__init__(
            "writing mode",
            options,
            ModeChange,
            draw_border=True,
            title="Choose you desired mode",
            section="mode",
            live_change=False,
        )
