from textual.app import ComposeResult, events
from textual.screen import Screen
from termtyper.ui.widgets.race_hud import RaceHUD
from termtyper.ui.widgets.screen import Typer


class TypingScreen(Screen):
    def on_mount(self):
        self.typer = Typer()
        self.hud = RaceHUD()

    def compose(self) -> ComposeResult:
        yield self.hud
        yield self.typer

    async def on_key(self, event: events.Key):
        key = event.character if (event.character) else event.key
        await self.typer.key_add(key)
