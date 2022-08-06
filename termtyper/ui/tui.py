import asyncio
from textual.app import App
from textual.widgets import Static
from textual import events
from termtyper.events.events import (
    BarThemeChange,
    LoadScreen,
    ModeChange,
    ParaSizeChange,
    TimeoutChange,
)

from termtyper.ui.settings_options import MenuSlide
from termtyper.ui.widgets.menu import Menu
from termtyper.ui.widgets.minimal_scrollview import MinimalScrollView
from termtyper.ui.widgets.menus import BarThemeMenu, ModeMenu, SizeMenu, TimeoutMenu

from ..ui.widgets import *  # NOQA
from ..utils import *  # NOQA

from ..utils.parser import MAIN_PARSER


def percent(part, total):
    return int(part * total / 100)


parser = MAIN_PARSER


class TermTyper(App):
    @classmethod
    def run(cls, quiet: bool = False):
        async def run_app() -> None:
            app = cls()
            app.quiet = quiet
            await app.process_messages()

        asyncio.run(run_app())

    async def on_load(self) -> None:
        self.current_space = "main_menu"
        self.settings = MenuSlide()
        self.size_menu = SizeMenu()
        self.timeout_menu = TimeoutMenu()
        self.mode_menu = ModeMenu()
        self.bar_theme_menu = BarThemeMenu()

        self.top = Static("")
        self.bottom = MinimalScrollView("")
        self.banner = Static(banners["welcome"])

        self.buttons = {
            "Start Typing!": self.load_typing_space,
            "Getting Started": self.load_getting_started,
            "Settings": self.load_settings,
            "Quit": self.action_quit,
        }
        self.main_menu = Menu(
            "buttons",
            list(self.buttons.keys()),
            ButtonClicked,
            draw_seperator=True,
            quiet=self.quiet,
        )

        self.race_hud = RaceHUD()
        self.typing_screen = Screen(self.quiet)

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
        await self.bottom.update(self.main_menu)
        self.refresh()

    async def load_getting_started(self):
        self.current_space = "getting_started"
        self.getting_started = GettingStarted()
        await self.top.update(GETTING_STARTERD_BANNER)
        await self.bottom.update(self.getting_started)

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
        await self.typing_screen._refresh_settings()
        self.race_hud.reset()
        await self.top.update(self.race_hud)
        await self.bottom.update(self.typing_screen)

    async def on_key(self, event: events.Key) -> None:
        match self.current_space:

            case "help_menu":
                if event.key in ["ctrl+h", "escape"]:
                    await self.load_settings()

            case "main_menu":
                await self.main_menu.key_press(event)

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
                    await self.bottom.key_press(event)

            case "mode_menu":
                await self.mode_menu.key_press(event)

            case "size_menu":
                await self.size_menu.key_press(event)

            case "timeout_menu":
                await self.timeout_menu.key_press(event)

            case "bar_theme_menu":
                await self.bar_theme_menu.key_press(event)

            case "typing_space":

                match event.key:
                    case "escape":
                        await self.load_main_menu()
                        await self.typing_screen.reset_screen()

                    case "ctrl+n":
                        parser.toggle_numbers()
                        await self.typing_screen.reset_screen()

                    case "ctrl+p":
                        parser.toggle_punctuations()
                        await self.typing_screen.reset_screen()

                    case "ctrl+d":
                        self.race_hud.toggle_details()

                    case "ctrl+s":
                        mode = parser.get("mode", "writing mode")
                        await self.typing_screen.reset_screen()
                        if mode == "words":
                            await self.bottom.update(self.size_menu)
                            self.current_space = "size_menu"
                        else:
                            await self.bottom.update(self.timeout_menu)
                            self.current_space = "timeout_menu"

                    case "ctrl+b":
                        await self.bottom.update(self.bar_theme_menu)
                        self.current_space = "bar_theme_menu"

                    case "ctrl+o":
                        await self.bottom.update(self.mode_menu)
                        self.current_space = "mode_menu"

                await self.typing_screen.key_add(event.key)

    async def handle_reset_hud(self, _: ResetHUD) -> None:
        self.race_hud.reset()

    async def handle_update_race_hud(self, event: UpdateRaceHUD) -> None:
        self.race_hud.update(event.completed, event.speed, event.accuracy)

    async def handle_mode_change(self, e: ModeChange):
        if e.mode is not None:
            parser.set("mode", "writing mode", e.mode)
            self.race_hud.reset()
            await self.typing_screen.reset_screen()

        await self.bottom.update(self.typing_screen)
        self.current_space = "typing_space"

    async def handle_bar_theme_change(self, e: BarThemeChange):
        if e.theme is not None:
            parser.set("theming", "bar_theme", e.theme)

        await self.bottom.update(self.typing_screen)
        self.race_hud.refresh()
        self.current_space = "typing_space"

    async def handle_timeout_change(self, e: TimeoutChange):
        if e.time is not None:
            parser.set("user", "timeout", e.time.split()[0])

        await self.bottom.update(self.typing_screen)
        await self.typing_screen.reset_screen()
        self.current_space = "typing_space"

    async def handle_para_size_change(self, e: ParaSizeChange):
        if e.length is not None:
            parser.set("user", "paragraph_size", e.length)

        await self.bottom.update(self.typing_screen)
        await self.typing_screen.reset_screen()
        self.current_space = "typing_space"

    async def handle_load_screen(self, e: LoadScreen):
        await eval(f"self.load_{e.screen}()")

    async def handle_button_clicked(self, e: ButtonClicked):
        if e.value:
            await self.buttons[e.value]()
