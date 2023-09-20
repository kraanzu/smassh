from textual.app import events
from textual.widget import Widget


class BaseScroll(Widget):
    DEFAULT_CSS = """
    BaseScroll {
        layout: vertical;
        overflow-y: scroll;
        height: 1fr;
        background: #2e3440;
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
