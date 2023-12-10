from textual.app import ComposeResult
from textual import events
from termtyper.ui.widgets.settings_options import menu
from termtyper.ui.widgets.base_scroll import BaseWindow


class SettingsScreen(BaseWindow):
    DEFAULT_CSS = """
    SettingsScreen {
        padding: 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_option = -1

    @property
    def current_setting(self):
        return menu[self.current_option]

    def compose(self) -> ComposeResult:
        for item in menu:
            yield item

    def on_key(self, event: events.Key):
        key = event.key
        n = len(menu)

        if key == "down":
            if self.current_option < n - 1:
                self.current_setting.remove_class("selected")
                self.current_option += 1
                self.current_setting.add_class("selected")
                self.current_setting.scroll_visible()
                self.refresh()

        elif key == "up":
            if self.current_option > 0:
                self.current_setting.remove_class("selected")
                self.current_option -= 1
                self.current_setting.add_class("selected")
                self.current_setting.scroll_visible()
                self.refresh()

        elif key == "tab":
            self.current_setting.select_next()

        elif key == "shift+tab":
            self.current_setting.select_prev()
