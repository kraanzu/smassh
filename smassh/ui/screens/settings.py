from textual.app import ComposeResult
from textual import events
from smassh.ui.widgets import menu
from smassh.ui.widgets import BaseWindow


class SettingsScreen(BaseWindow):
    DEFAULT_CSS = """
    SettingsScreen {
        padding: 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_option = 0

    @property
    def current_setting(self):
        return menu[self.current_option]

    def compose(self) -> ComposeResult:
        for item in menu:
            yield item

        self.update_highlight()

    def update_highlight(self):
        for index, setting in enumerate(menu):
            setting.set_class(index == self.current_option, "selected")

    async def handle_key(self, event: events.Key):
        key = event.key
        n = len(menu)

        await super().handle_key(event)

        if key in ["down", "j"]:
            if self.current_option < n - 1:
                self.current_option += 1
                self.update_highlight()
                self.current_setting.scroll_visible()
                self.refresh()

        elif key in ["up", "k"]:
            if self.current_option > 0:
                self.current_option -= 1
                self.update_highlight()
                self.current_setting.scroll_visible()
                self.refresh()

        elif key == "tab":
            self.current_setting.select_next()

        elif key == "shift+tab":
            self.current_setting.select_prev()
