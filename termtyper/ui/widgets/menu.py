from os import get_terminal_size
from rich.box import MINIMAL
from rich.tree import Tree
from rich.console import RenderableType
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from textual import events

from termtyper.events.events import ButtonClicked
from termtyper.ui.widgets.option import Option
from termtyper.utils.help_menu import percent
from termtyper.utils.play_keysound import get_sound_location, play


class Menu(Option):
    """
    A widget to show options in horizontal fashion
    with the selected option with a colored background
    """

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, new: int):
        total = len(self.options)
        self._cursor = max(0, min(new, total - 1))
        self.update()
        play(get_sound_location("mech"))

    async def key_press(self, event: events.Key):
        match event.key:
            case "j" | "down":
                self.select_next_option()
            case "k" | "up":
                self.select_prev_option()
            case "enter":
                await self.post_message(
                    ButtonClicked(self, self.options[self.cursor]),
                )

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
                tree, vertical="middle", height=percent(80, get_terminal_size()[1])
            ),
            border_style="magenta" if self._selected else "white",
            box=MINIMAL,
        )


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                Option("test", ["Linux", "MacPriceyOS", "YourPCRanIntoAnError"])
            )

    MyApp.run()
