from textual.app import ComposeResult
from textual import events
from textual.widget import Widget
from textual.containers import ScrollableContainer
from smassh.ui.widgets import menu
from smassh.ui.widgets import BaseWindow
from smassh.ui.widgets.settings.settings_options import Setting
from smassh.ui.widgets.settings import (
    SettingStrip,
    SettingStripItem,
    SettingSeparator,
    Bracket,
)


class SettingGrid(Widget):
    DEFAULT_CSS = """
    SettingGrid {
        layout: grid;
        grid-size: 1 2;
        grid-rows: 2 1fr;
    }
    """


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

        with SettingGrid():
            with SettingStrip():
                yield Bracket("left")
                for i in menu.keys():
                    yield SettingStripItem(i)
                yield Bracket("right")

            with ScrollableContainer():
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

        self.current_setting.scroll_visible()
        self.refresh()

    async def handle_key(self, event: events.Key) -> None:
        key = event.key
        n = len(self.settings)

        await super().handle_key(event)

        if key in ["down", "j"]:
            if self.current_option < n - 1:
                self.current_option += 1
                self.update_highlight()

        elif key in ["up", "k"]:
            if self.current_option > 0:
                self.current_option -= 1
                self.update_highlight()

        elif key == "tab":
            self.current_setting.select_next()

        elif key == "shift+tab":
            self.current_setting.select_prev()
