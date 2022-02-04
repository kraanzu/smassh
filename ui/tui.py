from rich.align import Align
from rich.text import Text, TextType
from textual.app import App
from textual.layouts.dock import DockLayout
from textual.widgets import Static, ScrollView
from textual import events

from rich.panel import Panel
from os import get_terminal_size as termsize

from ui.settings_options import menu
from ui.widgets import Button

percent = lambda part, total: int(part * total / 100)

welcome_message = """
╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐  ┌┬┐┌─┐  ┌┬┐┌─┐┬─┐┌┬┐┌┬┐┬ ┬┌─┐┌─┐  ┬
║║║├┤ │  │  │ ││││├┤    │ │ │   │ ├┤ ├┬┘│││ │ └┬┘├─┘├┤   │
╚╩╝└─┘┴─┘└─┘└─┘┴ ┴└─┘   ┴ └─┘   ┴ └─┘┴└─┴ ┴ ┴  ┴ ┴  └─┘  o
"""


class TermTyper(App):
    async def on_load(self):
        self.current_space = "settings"
        self.x, self.y = termsize()

        # FOR MAIN MENU
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

        # FOR SETTINGS
        self.total_items = len(menu)
        self.menus = list(menu.keys())
        self.current_menu_index = 0

    async def on_mount(self):
        await self.load_settings()
        pass

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

        self.current_menu = menu[self.current_menu_index]
        await self.view.dock(
            Static(
                Panel(
                    Align.center(
                        Text(menu[self.current_menu].ascii_art, style="bold blue"),
                        vertical="middle",
                    ),
                    style="black",
                    border_style="magenta",
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
                        Align.center(
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
        pass

    async def on_resize(self, _: events.Resize) -> None:
        await eval(f"self.load_{self.current_space}()")

    def on_key(self):
        pass

    async def handle_button_clicked(self, e: events.Click):
        if getattr(e.sender, "name") == "bt_quit":
            await self.action_quit()
