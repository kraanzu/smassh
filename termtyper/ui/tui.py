import webbrowser
from textual import on
from textual.app import App, ComposeResult, events
from textual.screen import Screen
from textual.widgets import ContentSwitcher
from termtyper.ui.events import SetScreen
from termtyper.ui.widgets import *  # noqa


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
            TypingSpace(id="typing"),
            AboutWidget(id="about"),
            SettingsWidget(id="settings"),
            HelpWidget(id="help"),
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
