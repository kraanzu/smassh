from os import get_terminal_size as termsize
from rich.align import Align

from textual.app import App
from textual.widgets import Static
from textual import events
from termtyper.events.events import BarThemeChange, LoadScreen, ParaSizeChange

from termtyper.ui.settings_options import MenuSlide
from termtyper.ui.widgets.menu import Menu
from termtyper.ui.widgets.minimal_scrollview import MinimalScrollView
from termtyper.ui.widgets.menus import BarThemeMenu, SizeMenu

from ..ui.widgets import *  # NOQA
from ..utils import *  # NOQA


def percent(part, total):
    return int(part * total / 100)


class TermTyper(App):
    async def on_load(self) -> None:
        self.parser = Parser()
        self.current_space = "main_menu"
        self.x, self.y = termsize()
        self.settings = MenuSlide()
        self.size_menu = SizeMenu()
        self.bar_theme_menu = BarThemeMenu()

        self.top = Static("hi")
        self.bottom = MinimalScrollView("")

        # FOR MAIN MENU
        self.banner = Static(banners["welcome"])

        self.buttons = {
            "Start Typing!": self.load_typing_space,
            "Getting Started": self.load_getting_started,
            "Settings": self.load_settings,
            "Quit": self.action_quit,
        }
        self.menu = Menu(
            "buttons",
            list(self.buttons.keys()),
            ButtonClicked,
            draw_seperator=True,
        )

        self.typing_screen = Screen()

        await self.bind("ctrl+q", "quit", "quit the application")

    async def on_mount(self) -> None:
        await self.setup_grid()
        await self.load_main_menu()
        self.set_interval(0.1, self.refresher)

    async def refresher(self):
        self.top.refresh()
        self.bottom.refresh()

    async def setup_grid(self):
        self.grid = await self.view.dock_grid()
        self.grid.add_row("top", size=8)
        self.grid.add_row("bottom")
        self.grid.add_column("col")
        self.grid.add_areas(top="col,top", bottom="col,bottom")
        self.grid.place(top=self.top, bottom=self.bottom)

    async def load_help_menu(self):
        await self.top.update(HELP_BANNER)
        await self.bottom.update(HELP_MESSAGE)
        self.current_space = "help_menu"

    async def load_main_menu(self) -> None:
        """
        Renders the Main Menu
        """
        self.current_space = "main_menu"
        await self.top.update(self.banner)
        await self.bottom.update(self.menu)
        self.refresh()

    async def load_getting_started(self):
        self.current_space = "getting_started"
        self.getting_started_scroll = Align.center(GETTING_STARTERD_MESSAGE)
        await self.top.update(GETTING_STARTERD_BANNER)
        await self.bottom.update(self.getting_started_scroll)

    async def load_settings(self):
        """
        Renders the Settings
        """

        await self.top.update(self.settings.banner())
        await self.bottom.update(self.settings)
        self.current_space = "settings"

    async def load_typing_space(self) -> None:
        """
        Renders the Typing Space
        """

        self.current_space = "typing_space"
        self.race_hud = RaceHUD()
        await self.typing_screen._refresh_settings()
        await self.top.update(self.race_hud)
        await self.bottom.update(self.typing_screen)

    async def on_key(self, event: events.Key) -> None:
        match self.current_space:

            case "help_menu":
                if event.key in ["ctrl+h", "escape"]:
                    await self.load_settings()

            case "main_menu":
                await self.menu.key_press(event)

            case "settings":
                if event.key == "ctrl+h":
                    await self.load_help_menu()
                else:
                    await self.settings.key_press(event)
                    await self.top.update(self.settings.banner())

            case "getting_started":
                if event.key == "escape":
                    await self.load_main_menu()
                else:
                    self.bottom.key_press(event)

            case "size_menu":
                await self.size_menu.key_press(event)

            case "bar_theme_menu":
                await self.bar_theme_menu.key_press(event)

            case "typing_space":
                if event.key == "escape":
                    await self.load_main_menu()
                    await self.typing_screen.reset_screen()
                    return

                if event.key == "ctrl+s":
                    await self.typing_screen.reset_screen()
                    await self.bottom.update(self.size_menu)
                    self.current_space = "size_menu"

                if event.key == "ctrl+b":
                    await self.bottom.update(self.bar_theme_menu)
                    self.current_space = "bar_theme_menu"

                if event.key == "ctrl+b":
                    await self.bottom.update(self.bar_theme_menu)
                    self.current_space = "bar_theme_menu"

                await self.typing_screen.key_add(event.key)

    async def handle_reset_hud(self, _: ResetHUD) -> None:
        self.race_hud.reset()

    async def handle_update_race_hud(self, event: UpdateRaceHUD) -> None:
        self.race_hud.update(event.completed, event.speed, event.accuracy)

    async def handle_bar_theme_change(self, e: BarThemeChange):
        await self.bottom.update(self.typing_screen)
        Parser().set_data("bar_theme", e.theme)
        self.current_space = "typing_space"

    async def handle_para_size_change(self, e: ParaSizeChange):
        await self.bottom.update(self.typing_screen)
        Parser().set_data("paragraph_size", e.length)
        await self.typing_screen.reset_screen()
        self.current_space = "typing_space"

    async def handle_load_screen(self, e: LoadScreen):
        await eval(f"self.load_{e.screen}()")

    async def handle_button_clicked(self, e: ButtonClicked):
        await self.buttons[e.value]()
