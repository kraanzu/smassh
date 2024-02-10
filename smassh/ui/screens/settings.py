from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual import events
from smassh.ui.widgets import menu
from smassh.ui.widgets import BaseWindow
from smassh.ui.widgets.settings.settings_options import Setting
from textual.widget import Widget


class SettingSeparator(Widget):
    DEFAULT_CSS = """
    SettingSeparator {
        height: auto;
        width: 100%;
        text-style: bold italic;
        margin: 1 0;
    }
    """

    COMPONENT_CLASSES = {"--primary-bg", "--danger-bg"}

    def __init__(self, section: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.section = section

    def render(self) -> RenderableType:
        classname = "danger" if "danger" in self.section else "primary"
        style = self.get_component_rich_style(f"--{classname}-bg")

        text = Text(self.section.upper(), style=style)
        text.pad(1)
        return text


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
