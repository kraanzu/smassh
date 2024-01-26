from typing import Optional
from textual.app import events
from textual.widget import Widget
from smassh.ui.events import SetScreen


class BaseWindow(Widget):
    """
    Base Window widget for content switcher
    """

    DEFAULT_CSS = """
    BaseWindow {
        layout: vertical;
        overflow-y: auto;
        height: 1fr;
        scrollbar-size: 1 1;
    }
    """

    async def handle_key(self, event: events.Key) -> Optional[bool]:
        if event.key == "escape":
            return self.post_message(SetScreen("typing"))
