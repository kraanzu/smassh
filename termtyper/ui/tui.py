import webbrowser
from textual import on
from textual.app import App, ComposeResult, events
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import ContentSwitcher
from termtyper.ui.css import CSS
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
    DEFAULT_CSS = CSS

    async def on_mount(self):
        self.push_screen(MainScreen())

    async def on_ready(self):
        self.action_theme(config_parser.theme)

    def action_sponsor(self):
        webbrowser.open("https://github.com/sponsors/kraanzu")

    def action_theme(self, theme: str):
        def remove_existing_theme(w: Widget):
            for name in w.classes:
                if name.startswith("theme-"):
                    w.remove_class(name)
                    return

        with self.batch_update():
            for widget in self.query("*"):
                remove_existing_theme(widget)
                widget.add_class(f"theme-{theme}")
