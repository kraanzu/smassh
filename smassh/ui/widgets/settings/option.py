from typing import Callable, List, Optional
from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from smassh.src import config_parser
from smassh.ui.widgets.typing.space import Space


class BaseOption(Widget):
    """
    Base Option Widget to extent from for setting
    """

    DEFAULT_CSS = """
    BaseOption {
        align: center middle;
        content-align: center middle;
        padding: 0 1;
    }
    """

    def __init__(self, setting_name: str, callback: Optional[Callable] = None) -> None:
        super().__init__(id=f"option-{setting_name}")
        self.setting_name = setting_name
        self._callback = callback

    def on_mount(self) -> None:
        self.load_current_setting()

    def callback(self) -> None:
        if self._callback:
            return self._callback()

        return self.app.query_one(Space).reset()

    @property
    def value(self) -> str:
        raise NotImplementedError

    def highlight(self) -> None:
        pass

    def lowlight(self) -> None:
        pass

    def _select_next_option(self) -> None:
        pass

    def _select_prev_option(self) -> None:
        pass

    def select_next_option(self) -> None:
        self._select_next_option()
        self.save()

    def select_prev_option(self) -> None:
        self._select_prev_option()
        self.save()

    def save(self) -> None:
        config_parser.set(self.setting_name, self.value)
        self.callback()

    def load_current_setting(self) -> None:
        raise NotImplementedError


class OptionItem(Widget):
    """
    Widget for sigle option in `Option` widget
    """

    DEFAULT_CSS = """
    OptionItem {
        height: 1;
        width: auto;
        padding: 0 1;
    }
    """

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def render(self) -> RenderableType:
        return self.value


class Option(BaseOption):
    """
    Option Widget for choosing between multiple options
    """

    def __init__(
        self,
        setting_name: str,
        options: List[str],
        callback: Optional[Callable] = None,
    ) -> None:
        self.options = [OptionItem(option) for option in options]
        self._value = 0
        super().__init__(setting_name, callback)

    def load_current_setting(self) -> None:
        setting = config_parser.get(self.setting_name)
        if isinstance(setting, bool):
            setting = ["off", "on"][setting]

        option = [i for i in self.options if i.value == setting][0]
        self._value = self.options.index(option)
        self.update_highlight()

    @property
    def value(self) -> str:
        return self.options[self._value].value

    def update_highlight(self) -> None:
        for i, option in enumerate(self.options):
            option.set_class(i == self._value, "selected")

    def _select_next_option(self) -> None:
        n = len(self.options)
        self._value = (self._value + 1) % n
        self.update_highlight()

    def _select_prev_option(self) -> None:
        n = len(self.options)
        self._value = (self._value - 1 + n) % n
        self.update_highlight()

    def compose(self) -> ComposeResult:
        for option in self.options:
            yield option


class NumberScroll(BaseOption):
    """
    Widget for setting numeric value for a setting
    """

    COMPONENT_CLASSES = {"scroll--background"}

    def __init__(
        self,
        setting_name: str,
        callback: Optional[Callable] = None,
    ) -> None:
        super().__init__(setting_name, callback)
        self._value = 0

    @property
    def value(self) -> int:
        return self._value

    def load_current_setting(self) -> None:
        value = config_parser.get(self.setting_name)
        self._value = value

    def _select_next_option(self) -> None:
        self._value = min(self._value + 1, 100)
        self.refresh()

    def _select_prev_option(self) -> None:
        self._value = max(self._value - 1, 0)
        self.refresh()

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("scroll--background")
        text = Text(str(self.value), style=style)
        text.pad(2)
        return text
