from typing import List
from textual.app import ComposeResult
from textual import events
from textual.widget import Widget
from textual.widgets import Static
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


class SettingsContainer(Widget):
    DEFAULT_CSS = """
    SettingsContainer {
        width: 1fr;
        height: 1fr;
        layout: vertical;
        overflow: auto auto;
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
        self.sections: List[SettingStripItem] = []
        self.settings: List[Setting] = []

        for section, settings in menu.items():
            self.sections.append(SettingStripItem(section))
            self.settings.extend(settings)

    @property
    def current_setting(self) -> Setting:
        return self.settings[self.current_option]

    def get_section(self, setting: Setting) -> str:
        for section, settings in menu.items():
            if setting in settings:
                return section

        raise ValueError(f"Setting {setting} not found in menu")

    def compose(self) -> ComposeResult:

        with SettingGrid():
            with SettingStrip():
                yield Bracket("left")
                yield from self.sections
                yield Bracket("right")

            with SettingsContainer():
                for section, settings in menu.items():
                    with Static() as container:
                        yield SettingSeparator(section)
                        settings[0].set_section_widget(container)
                        yield settings[0]

                    for setting in settings[1:]:
                        yield setting

        self.update_highlight()

    def update_highlight_strip(self, section_name: str) -> None:
        for section in self.sections:
            section.set_class(section.section == section_name, "enabled")

    def update_highlight(self) -> None:
        """
        Automatically update highlights based on current option
        """

        for index, setting in enumerate(self.settings):
            is_current = index == self.current_option
            setting.set_class(is_current, "selected")
            if is_current:
                self.update_highlight_strip(self.get_section(setting))

        section = self.get_section(self.current_setting)
        if self.current_setting == menu[section][0]:
            self.current_setting.section_widget.scroll_visible()
        else:
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
