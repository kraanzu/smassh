import webbrowser
from textual import on
from textual.app import App, ComposeResult, events
from textual.screen import Screen
from textual.widgets import ContentSwitcher
from termtyper.ui.events import SetScreen, ShowResults
from termtyper.ui.widgets import *  # noqa
from termtyper.ui.screens import *  # noqa
from termtyper.ui.widgets.palette.palette_list import ApplyLanguage, ApplyTheme
from termtyper.ui.widgets.palette import LanguagePalette, ThemePalette
from termtyper.src import config_parser, generate_theme_file, data_parser
from termtyper.ui.widgets import Space, Ticker


class MainScreen(Screen):
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
    def screen_change(self, event: SetScreen):
        self.query_one(ContentSwitcher).current = event.screen_name
        self.query_one(Header).set_active(event.screen_name)

    @on(ShowResults)
    def show_results(self, event: ShowResults):
        # reset all watching timers
        space = self.query_one(Space)
        space.check_timer.pause()
        space.tracker.stats.finish()
        self.query_one(Ticker).reset()

        self.query_one(ContentSwitcher).current = "result"
        self.query_one(ResultScreen).set_results(event.stats)

        if not event.failed:
            data_parser.add_stats(event.stats)

    async def handle_key(self, event: events.Key):
        visible = self.query_one(ContentSwitcher).visible_content
        if visible:
            await visible.handle_key(event)


class TermTyper(App):
    CSS_PATH = "css/styles.tcss"
    SCREENS = {
        "main": MainScreen(),
        "theme": ThemePaletteScreen(),
        "language": LanguagePaletteScreen(),
    }

    def __init__(self, *args, **kwargs):
        self.action_theme(config_parser.get("theme"))
        super().__init__(*args, **kwargs, watch_css=True)

    async def _on_css_change(self) -> None:
        await super()._on_css_change()
        self.refresh_css()

    async def on_mount(self):
        self.push_screen("main")

    @on(ApplyLanguage)
    def apply_language(self, event: ApplyLanguage):
        config_parser.set("language", event.value)
        self.SCREENS["main"].query_one(LanguagePalette).refresh()
        self.SCREENS["main"].query_one(Space).reset()

    @on(ApplyTheme)
    def apply_theme(self, event: ApplyTheme):
        self.action_theme(event.value)
        config_parser.set("theme", event.value)
        self.SCREENS["main"].query_one(ThemePalette).refresh()

    def action_star(self):
        webbrowser.open("https://github.com/kraanzu/termtyper")

    def action_theme(self, theme: str):
        generate_theme_file(theme)
