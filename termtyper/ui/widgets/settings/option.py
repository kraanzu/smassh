from typing import Callable, List, Optional
from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from termtyper.src import config_parser
from termtyper.ui.widgets.typing.space import Space


class BaseOption(Widget):

    DEFAULT_CSS = """
    BaseOption {
        align: center middle;
        content-align: center middle;
        padding: 0 1;
    }
    """

    def __init__(self, setting_name: str, callback: Optional[Callable] = None):
        super().__init__(id=f"option-{setting_name}")
        self.setting_name = setting_name
        self._callback = callback

    def on_mount(self):
        self.load_current_setting()

    def callback(self):
        if self._callback:
            return self._callback()

        return self.app.query_one(Space).reset()

    @property
    def value(self):
        raise NotImplementedError

    def highlight(self):
        pass

    def lowlight(self):
        pass

    def _select_next_option(self):
        pass

    def _select_prev_option(self):
        pass

    def select_next_option(self):
        self._select_next_option()
        self.save()

    def select_prev_option(self):
        self._select_prev_option()
        self.save()

    def save(self):
        config_parser.set(self.setting_name, self.value)
        self.callback()

    def load_current_setting(self):
        raise NotImplementedError


class OptionItem(Widget):
    DEFAULT_CSS = """
    OptionItem {
        height: 1;
        width: auto;
        padding: 0 1;
    }
    """

    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def render(self) -> RenderableType:
        return self.value


class Option(BaseOption):
    def __init__(
        self,
        setting_name: str,
        options: List[str],
        callback: Optional[Callable] = None,
    ):
        self.options = [OptionItem(option) for option in options]
        self._value = 0
        super().__init__(setting_name, callback)

    def load_current_setting(self):
        setting = config_parser.get(self.setting_name)
        if isinstance(setting, bool):
            setting = ["off", "on"][setting]

        option = [i for i in self.options if i.value == setting][0]
        self._value = self.options.index(option)
        self.update_highlight()

    @property
    def value(self):
        return self.options[self._value].value

    def update_highlight(self):
        for i, option in enumerate(self.options):
            option.set_class(i == self._value, "selected")

    def _select_next_option(self):
        n = len(self.options)
        self._value = (self._value + 1) % n
        self.update_highlight()

    def _select_prev_option(self):
        n = len(self.options)
        self._value = (self._value - 1 + n) % n
        self.update_highlight()

    def compose(self) -> ComposeResult:
        for option in self.options:
            yield option


class NumberScroll(BaseOption):
    COMPONENT_CLASSES = {"scroll--background"}

    def __init__(
        self,
        setting_name: str,
        callback: Optional[Callable] = None,
    ):
        super().__init__(setting_name, callback)
        self._value = 0

    @property
    def value(self):
        return self._value

    def load_current_setting(self):
        value = config_parser.get(self.setting_name)
        self._value = value

    def _select_next_option(self):
        self._value = min(self._value + 1, 100)
        self.refresh()

    def _select_prev_option(self):
        self._value = max(self._value - 1, 0)
        self.refresh()

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("scroll--background")
        text = Text(str(self.value), style=style)
        text.pad(2)
        return text
