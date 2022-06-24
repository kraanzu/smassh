from typing import Callable
from rich.box import HEAVY
from rich.tree import Tree
from rich.console import RenderableType
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from textual import events
from textual.widget import Widget

from ...utils import Parser


class Option(Widget):
    """
    A widget to show options in horizontal fashion
    with the selected option with a colored background
    """

    def __init__(
        self, name: str, options: list[str], callback: Callable = lambda: None
    ) -> None:
        super().__init__()
        self.name = name
        self.options = [i.strip() for i in options]
        self._max_len = max(len(i) for i in self.options)
        self._cursor = self.options.index(Parser().get_data(self.name))
        self.callback = callback
        self._selected = False

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
        self.update()

    def highlight(self) -> None:
        self.selected = True

    def lowlight(self) -> None:
        self.selected = False

    def update(self) -> None:
        Parser().set_data(self.name, self.options[self._cursor])

        if self.callback:
            self.callback()

        self.refresh()

    def select_next_option(self) -> None:
        self.cursor += 1

    def select_prev_option(self) -> None:
        self.cursor -= 1

    async def on_mouse_scroll_down(self, _: events.MouseScrollDown) -> None:
        self.select_prev_option()

    async def on_mouse_scroll_up(self, _: events.MouseScrollUp) -> None:
        self.select_next_option()

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        for index, i in enumerate(self.options):
            label = Text(i.ljust(self._max_len))

            if index == self._cursor:
                label.stylize("b green")
                label += " "

            tree.add(label)

        return Panel(
            Align.center(
                tree,
                vertical="middle",
            ),
            border_style="magenta" if self._selected else "white",
            box=HEAVY,
        )


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                Option("test", ["Linux", "MacPriceyOS", "YourPCRanIntoAnError"])
            )

    MyApp.run()
