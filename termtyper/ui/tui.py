from textual.app import App
from termtyper.ui.screens import *  # noqa


class TermTyper(App):
    SCREENS = {
        "typing": TypingScreen(name="typing"),
        "settings": SettingsScreen(name="settings"),
        "about": AboutScreen(name="about"),
        "help": HelpScreen(name="help"),
    }

    async def on_mount(self):
        self.app.push_screen("typing")
