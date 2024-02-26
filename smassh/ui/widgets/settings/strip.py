from rich.console import RenderableType
from textual.widget import Widget
from textual.widgets import Label
from smassh.ui.widgets.settings.settings_options import menu


class SettingStripItem(Label):
    DEFAULT_CSS = """
    SettingStripItem {
        color: white;
        padding: 0 2;
        height: 1;
    }
    """

    def __init__(self, section: str, *args, **kwargs) -> None:
        super().__init__(section, *args, **kwargs)
        self.section = section

    def render(self) -> RenderableType:
        return self.section.replace("_", " ")

    def on_click(self) -> None:
        from smassh.ui.screens import SettingsScreen

        settings_screen = self.screen.query_one(SettingsScreen)
        settings = settings_screen.settings
        first_setting = menu[self.section][0]
        settings_screen.current_option = settings.index(first_setting)
        settings_screen.update_highlight()


class SettingStrip(Widget):
    DEFAULT_CSS = """
    SettingStrip {
        height: 2;
        layout: horizontal;
        width: 100%;
        align: center top;
    }
    """
