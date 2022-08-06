from typing import Callable, Literal
from rich import box
from rich.tree import Tree
from rich.console import RenderableType
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from textual import events
from textual.widget import Widget

from ...utils.parser import MAIN_PARSER

parser = MAIN_PARSER
SectionType = Literal[
    "user", "theming", "paragraph", "speed records word", "speed records time"
]


class Option(Widget):
    """
    A widget to show options in horizontal fashion
    with the selected option with a colored background
    """

    def __init__(
        self,
        name: str,
        options: list[str],
        callback: Callable = lambda: None,
        section: SectionType | None = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.options = [i.strip() for i in options]
        self._max_len = max(len(i) for i in self.options)
        self.section = section
        self.callback = callback
        self._selected = False
        self.reset_cursor()

    def reset_cursor(self):
        if self.section:
            self._cursor = self.options.index(parser.get(self.section, self.name))
        else:
            self._cursor = 0

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, new: int):
        total = len(self.options)
        self._cursor = max(0, min(new, total - 1))
        self.update()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, new: bool):
        self._selected = new

    def highlight(self) -> None:
        self.selected = True

    def lowlight(self) -> None:
        self.selected = False

    def update(self) -> None:
        if self.section:
            parser.set(self.section, self.name, self.options[self.cursor])

        if self.callback:
            self.callback()

        self.refresh()

    def select_next_option(self) -> None:
        self.cursor += 1

    def select_prev_option(self) -> None:
        self.cursor -= 1

    async def key_press(self, event: events.Key):
        match event.key:
            case "j" | "down":
                self.select_next_option()
            case "k" | "up":
                self.select_prev_option()

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        for index, i in enumerate(self.options):
            label = Text(i.ljust(self._max_len))
            label.pad(1)

            if index == self._cursor:
                label.stylize("r green")

            tree.add(label)

        return Panel(
            Align.center(
                tree,
                vertical="middle",
            ),
            border_style="magenta" if self.selected else "white",
            height=8,
            box=box.HEAVY,
        )


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                Option("test", ["Linux", "MacPriceyOS", "YourPCRanIntoAnError"])
            )

    MyApp.run()
