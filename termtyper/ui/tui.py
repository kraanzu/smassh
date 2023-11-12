import webbrowser
from textual import on
from textual.app import App, ComposeResult, events
from textual.screen import Screen
from textual.widgets import ContentSwitcher
from termtyper.ui.events import SetScreen
from termtyper.ui.widgets import *  # noqa
from termtyper.ui.screens import *  # noqa


class BaseScreen(Screen):
    DEFAULT_CSS = """
    BaseScreen {
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
            initial="about",
        )

    @on(SetScreen)
    def screen_change(self, event: SetScreen):
        self.query_one(ContentSwitcher).current = event.screen_name

    def on_key(self, event: events.Key):
        visible = self.query_one(ContentSwitcher).visible_content
        if visible:
            visible.on_key(event)


class TermTyper(App):
    async def on_mount(self):
        self.push_screen(BaseScreen())

    def action_sponsor(self):
        webbrowser.open("https://github.com/sponsors/kraanzu")
