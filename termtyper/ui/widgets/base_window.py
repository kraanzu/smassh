from textual.app import events
from textual.widget import Widget
from termtyper.ui.events import SetScreen


class BaseWindow(Widget):
    DEFAULT_CSS = """
    BaseWindow {
        layout: vertical;
        overflow-y: auto;
        height: 1fr;
        scrollbar-size: 1 1;
    }
    """

    async def handle_key(self, event: events.Key):
        if event.key == "escape":
            return self.post_message(SetScreen("typing"))
