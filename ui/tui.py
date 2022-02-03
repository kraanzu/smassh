from rich.align import Align
from rich.text import Text
from textual.app import App
from textual.layouts.dock import DockLayout
from textual.widgets import Static
from textual import events

from rich.panel import Panel
from os import get_terminal_size as termsize

from widgets.button import Button

percent = lambda part, total: int(part * total / 100)

welcome_message = """
╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐  ┌┬┐┌─┐  ┌┬┐┌─┐┬─┐┌┬┐┌┬┐┬ ┬┌─┐┌─┐  ┬
║║║├┤ │  │  │ ││││├┤    │ │ │   │ ├┤ ├┬┘│││ │ └┬┘├─┘├┤   │
╚╩╝└─┘┴─┘└─┘└─┘┴ ┴└─┘   ┴ └─┘   ┴ └─┘┴└─┴ ┴ ┴  ┴ ┴  └─┘  o
"""


class TermType(App):
    async def on_mount(self):
        self.current_space = "main_menu"
        self.x, self.y = termsize()

        self.banner = Static(
            Panel(
                Align.center(
                    Text(welcome_message, style="bold blue"), vertical="middle"
                ),
                style="black",
                border_style="magenta",
            )
        )
        self.bt_typing_space = Button(
            label="Start Typing !".center(30),
            name="bt_typing_space",
        )
        self.bt_settings = Button(label="Settings".center(30), name="bt_settings")
        self.bt_quit = Button(label="Quit".center(30), name="bt_quit")

        await self.load_main_menu()

    async def clear_screen(self):
        if isinstance(self.view.layout, DockLayout):
            self.view.layout.docks.clear()
        self.view.widgets.clear()

    async def load_main_menu(self):
        await self.clear_screen()
        await self.view.dock(self.banner, size=percent(30, self.y))
        await self.view.dock(self.bt_typing_space, self.bt_settings, self.bt_quit)

    async def load_settings(self):
        pass

    async def load_typing_space(self):
        pass

    def on_key(self):
        pass

    async def handle_button_clicked(self, e: events.Click):
        if getattr(e.sender, "name") == "bt_quit":
            await self.action_quit()


TermType.run()
