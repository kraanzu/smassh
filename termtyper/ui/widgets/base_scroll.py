from textual.app import events
from textual.widget import Widget


class BaseWindow(Widget):
    DEFAULT_CSS = """
    BaseWindow {
        layout: vertical;
        overflow-y: auto;
        height: 1fr;
        scrollbar-size: 1 1;
    }
    """

    def on_key(self, event: events.Key):
        key = event.key

        if key in ["j", "down"]:
            self.scroll_down()
        elif key in ["k", "up"]:
            self.scroll_up()
        elif key in ["g", "home"]:
            self.scroll_home()
        elif key in ["G", "end"]:
            self.scroll_end()
