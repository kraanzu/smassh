from textual.app import ComposeResult
from textual import events
from smassh.ui.widgets import menu
from smassh.ui.widgets import BaseWindow
from smassh.ui.widgets.settings.settings_options import Setting
from smassh.ui.widgets.settings import (
    SettingStrip,
    SettingStripItem,
    SettingSeparator,
    Bracket,
)


class SettingsScreen(BaseWindow):
    """
    Setting Screen to show all the tweakables!
    """

    DEFAULT_CSS = """
    SettingsScreen {
        padding: 1;
    }
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_option = 0
        self.settings = []
        for settings in menu.values():
            self.settings.extend(settings)

    @property
    def current_setting(self) -> Setting:
        return self.settings[self.current_option]

    def compose(self) -> ComposeResult:
        with SettingStrip():
            yield Bracket("left")
            for i in menu.keys():
                yield SettingStripItem(i)
            yield Bracket("right")

        for section, settings in menu.items():
            yield SettingSeparator(section)
            for setting in settings:
                yield setting

        self.update_highlight()

    def update_highlight(self) -> None:
        """
        Automatically update highlights based on current option
        """

        for index, setting in enumerate(self.settings):
            setting.set_class(index == self.current_option, "selected")

    async def handle_key(self, event: events.Key) -> None:
        key = event.key
        n = len(self.settings)

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
