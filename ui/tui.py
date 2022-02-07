from rich.align import Align
from rich.box import HEAVY_EDGE
from rich.text import Text, TextType
from textual.app import App
from textual.layouts.dock import DockLayout
from textual.widgets import Static, ScrollView
from textual import events

from rich.panel import Panel
from os import get_terminal_size as termsize, supports_dir_fd

from ui.settings_options import menu
from ui.widgets import Button, RaceBar, Screen
from utils import Parser

percent = lambda part, total: int(part * total / 100)

welcome_message = """
╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐  ┌┬┐┌─┐  ┌┬┐┌─┐┬─┐┌┬┐┌┬┐┬ ┬┌─┐┌─┐  ┬
║║║├┤ │  │  │ ││││├┤    │ │ │   │ ├┤ ├┬┘│││ │ └┬┘├─┘├┤   │
╚╩╝└─┘┴─┘└─┘└─┘┴ ┴└─┘   ┴ └─┘   ┴ └─┘┴└─┴ ┴ ┴  ┴ ┴  └─┘  o
"""


class TermTyper(App):
    async def on_load(self):
        self.parser = Parser()
        self.current_space = "main_menu"
        self.x, self.y = termsize()

        # FOR MAIN MENU
        self.banner = Static(
            Panel(
                Align.center(
                    Text(welcome_message, style="bold blue"), vertical="middle"
                ),
                style="black",
                border_style="magenta",
                box=HEAVY_EDGE,
            )
        )
        self.bt_typing_space = Button(
            label="Start Typing !".center(30),
            name="bt_typing_space",
        )
        self.bt_settings = Button(label="Settings".center(30), name="bt_settings")
        self.bt_quit = Button(label="Quit".center(30), name="bt_quit")

        # FOR SETTINGS
        self.menus = list(menu.keys())
        self.current_menu_index = 0

        # FOR TYPING SPACE
        self.race_bar = RaceBar()

    async def on_mount(self):
        await self.load_main_menu()

    async def clear_screen(self):
        if isinstance(self.view.layout, DockLayout):
            self.view.layout.docks.clear()
        self.view.widgets.clear()

    async def load_main_menu(self):
        await self.clear_screen()
        await self.view.dock(self.banner, size=percent(30, self.y))
        await self.view.dock(
            self.bt_typing_space,
            self.bt_settings,
            self.bt_quit,
            size=percent(25, self.y),
        )
        self.current_space = "main_menu"

    async def load_settings(self):
        await self.clear_screen()

        self.current_menu = self.menus[self.current_menu_index]
        await self.view.dock(
            Static(
                Panel(
                    Align.center(
                        Text(menu[self.current_menu].ascii_art, style="bold blue"),
                        vertical="middle",
                    ),
                    style="black",
                    border_style="bold magenta",
                    subtitle="Press L/R arrow keys to navigate through different menus",
                    subtitle_align="left",
                )
            ),
            size=percent(20, self.y),
        )

        item_count = len(menu[self.current_menu].items)
        grid = await self.view.dock_grid(gutter=(1, 1))
        grid.add_column("desc", fraction=2)
        grid.add_column("value")
        grid.add_row("row", repeat=item_count)

        count = item_count + 1
        grid.add_areas(**{f"item{i}": f"desc,row{i}" for i in range(1, count)})
        grid.add_areas(**{f"val{i}": f"value,row{i}" for i in range(1, count)})

        grid.place(
            **{
                f"item{i}": Static(
                    Panel(
                        Align.left(
                            menu[self.current_menu].items[i - 1].description,
                            vertical="middle",
                        )
                    )
                )
                for i in range(1, count)
            }
        )
        grid.place(
            **{
                f"val{i}": menu[self.current_menu].items[i - 1].widget
                for i in range(1, count)
            }
        )

        self.current_space = "settings"

    async def load_typing_space(self):
        await self.clear_screen()

        self.typing_screen = Screen()
        self.current_space = "typing_space"
        await self.view.dock(self.race_bar, size=percent(20, self.y))
        await self.view.dock(self.typing_screen)

    async def on_resize(self, _: events.Resize) -> None:
        await eval(f"self.load_{self.current_space}()")

    async def on_key(self, event: events.Key):

        if self.current_space == "settings":
            match event.key:
                case "right":
                    self.current_menu_index = (self.current_menu_index + 1) % len(menu)
                    await self.load_settings()

                case "left":
                    self.current_menu_index = (
                        self.current_menu_index + len(menu) - 1
                    ) % len(menu)
                    await self.load_settings()

                case "escape":
                    await self.load_main_menu()
        else:
            await self.typing_screen.key_add(event.key)

    async def handle_update_race_bar(self, event):
        self.race_bar.update(event.completed, event.speed)

    async def handle_button_clicked(self, e: events.Click):
        if getattr(e.sender, "name") == "bt_quit":
            await self.action_quit()
        elif getattr(e.sender, "name") == "bt_settings":
            await self.load_settings()
        elif getattr(e.sender, "name") == "bt_typing_space":
            await self.load_typing_space()
