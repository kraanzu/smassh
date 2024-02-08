import webbrowser
from textual import on
from textual.app import App, ComposeResult, events
from textual.screen import Screen
from textual.widgets import ContentSwitcher
from smassh.ui.events import SetScreen, ShowResults
from smassh.ui.widgets import *  # noqa
from smassh.ui.screens import *  # noqa
from smassh.ui.widgets.palette.palette_list import ApplyLanguage, ApplyTheme
from smassh.ui.widgets.palette import LanguagePalette, ThemePalette
from smassh.src import config_parser, generate_theme_file, data_parser
from smassh.ui.widgets import Space, Ticker


class MainScreen(Screen):
    """
    Main Screen which renders all the first visible option when app starts
    """

    DEFAULT_CSS = """
    MainScreen {
        layout: grid;
        grid-size: 1 2;
        grid-rows: 5 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield ContentSwitcher(
            TypingScreen(id="typing"),
            AboutScreen(id="about"),
            SettingsScreen(id="settings"),
            HelpScreen(id="help"),
            ResultScreen(id="result"),
            # initial screen
            initial="typing",
        )

    @on(SetScreen)
    def screen_change(self, event: SetScreen) -> None:
        """
        Change BaseWidget in the main screen depending on name

        Args:
            event (SetScreen): event with screen name
        """

        self.query_one(ContentSwitcher).current = event.screen_name
        self.query_one(Header).set_active(event.screen_name)

    @on(ShowResults)
    def show_results(self, event: ShowResults) -> None:
        """
        Triggered when typing is finished

        Args:
            event (ShowResults): Event containing stats and if it the typing was a failed attempt
        """

        # reset all watching timers
        space = self.query_one(Space)
        space.check_timer.pause()
        space.tracker.stats.finish()
        self.query_one(Ticker).reset()

        self.query_one(ContentSwitcher).current = "result"
        self.query_one(ResultScreen).set_results(event.stats)

        data_parser.add_stats(event.stats, event.failed)

    async def handle_key(self, event: events.Key) -> None:
        visible = self.query_one(ContentSwitcher).visible_content
        if visible:
            await visible.handle_key(event)


class Smassh(App):
    CSS_PATH = "css/styles.tcss"
    SCREENS = {
        "main": MainScreen(),
        "theme": ThemePaletteScreen(),
        "language": LanguagePaletteScreen(),
    }

    def __init__(self, *args, **kwargs) -> None:
        self.action_theme(config_parser.get("theme"))
        super().__init__(*args, **kwargs, watch_css=True)

    async def _on_css_change(self) -> None:
        await super()._on_css_change()
        self.refresh_css()

    async def on_mount(self) -> None:
        self.push_screen("main")

    @on(ApplyLanguage)
    def apply_language(self, event: ApplyLanguage) -> None:
        config_parser.set("language", event.value)
        self.SCREENS["main"].query_one(LanguagePalette).refresh()
        self.SCREENS["main"].query_one(Space).reset()

    @on(ApplyTheme)
    def apply_theme(self, event: ApplyTheme) -> None:
        self.action_theme(event.value)
        config_parser.set("theme", event.value)
        self.SCREENS["main"].query_one(ThemePalette).refresh()

    def action_star(self) -> None:
        webbrowser.open("https://github.com/kraanzu/smassh")

    def action_theme(self, theme: str) -> None:
        generate_theme_file(theme)
