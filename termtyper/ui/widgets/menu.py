from os import get_terminal_size
from typing import Callable
from rich.box import HEAVY, MINIMAL
from rich.tree import Tree
from rich.console import RenderableType
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from textual import events

from termtyper.ui.widgets.option import Option
from termtyper.utils.help_menu import percent
from termtyper.utils.play_keysound import get_sound_location, play

HEIGHT = round(0.8 * get_terminal_size()[1])


seperator = Text("─" * 35, style="bold dim black")


class Menu(Option):
    """
    A widget to show options in horizontal fashion
    with the selected option with a colored background
    """

    def __init__(
        self,
        name: str,
        options: list[str],
        message: Callable,
        draw_border: bool = False,
        draw_seperator: bool = False,
        title: str = "",
        section: str | None = None,
        live_change: bool = True,
        quiet: bool = False,
    ) -> None:
        super().__init__(name, options, section=section)
        self.message = message
        self.draw_border = draw_border
        self.draw_seperator = draw_seperator
        self.title = title
        self.live_change = live_change
        self.fallback = None
        self.quiet = quiet

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, new: int):
        total = len(self.options)
        self._cursor = max(0, min(new, total - 1))

        if self.live_change:
            self.update()

        if not self.quiet:
            play(get_sound_location("mech"))

        self.refresh()

    async def key_press(self, event: events.Key):

        if self.fallback is None:
            self.fallback = self.cursor

        match event.key:
            case "j" | "down":
                self.select_next_option()
            case "k" | "up":
                self.select_prev_option()
            case "enter":
                await self.post_message(
                    self.message(self, self.options[self.cursor]),
                )
                self.fallback = None
            case "escape":
                await self.post_message(self.message(self))
                self.cursor = self.fallback
                self.fallback = None

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        for index, i in enumerate(self.options):
            label = Text(i.ljust(self._max_len))

            if index == self._cursor:
                label.stylize("b green")
                label = Text("> ") + label
            else:
                label = Text("  ") + label

            tree.add(Align.center(label))
            if self.draw_seperator:
                tree.add(Align.center(seperator))

        return self.render_panel(tree)

    def render_panel(self, tree) -> RenderableType:
        return Align.center(
            Panel(
                tree,
                box=HEAVY if self.draw_border else MINIMAL,
                expand=False,
                title=self.title,
            ),
            vertical="middle",
            height=percent(80, get_terminal_size()[1]),
        )


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                Option("test", ["Linux", "MacPriceyOS", "YourPCRanIntoAnError"])
            )

    MyApp.run()
