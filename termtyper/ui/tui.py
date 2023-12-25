import shutil
from pathlib import Path
import webbrowser
from textual import on
from textual.app import App, ComposeResult, events
from textual.screen import Screen
from textual.widgets import ContentSwitcher
from termtyper.ui.events import SetScreen
from termtyper.ui.widgets import *  # noqa
from termtyper.ui.screens import *  # noqa
from termtyper.src.parser import config_parser


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
            # initial screen
            initial="typing",
        )

    @on(SetScreen)
    def screen_change(self, event: SetScreen):
        self.query_one(ContentSwitcher).current = event.screen_name

    def on_key(self, event: events.Key):
        visible = self.query_one(ContentSwitcher).visible_content
        if visible:
            visible.on_key(event)


class TermTyper(App):
    CSS_PATH = "css/styles.tcss"
    SCREENS = {
        "main": MainScreen(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, watch_css=True)

    async def on_mount(self):
        self.push_screen("main")
        self.action_theme(config_parser.get("theme"))

    def action_sponsor(self):
        webbrowser.open("https://github.com/sponsors/kraanzu")

    def action_theme(self, theme: str):
        css_folder = Path.absolute(Path(__file__).parent.parent) / "ui" / "css"
        themes_folder = css_folder / "themes"

        base_css = css_folder / "styles.tcss"
        theme_path = themes_folder / f"{theme}.tcss"

        shutil.copy(theme_path, base_css)
