from typing import List
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget
from termtyper.src.parser import config_parser


class BaseOption(Widget):

    DEFAULT_CSS = """
    BaseOption {
        align: center middle;
        content-align: center middle;
        padding: 0 1;
    }
    """

    def __init__(self, setting_name: str):
        super().__init__()
        self.setting_name = setting_name

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
    def __init__(self, setting_name: str, options: List[str]):
        super().__init__(setting_name)
        self.options = [OptionItem(option) for option in options]
        self._value = 0

    @property
    def value(self):
        return self.options[self._value].value

    def update_highlight(self):
        for i, option in enumerate(self.options):
            option.set_class(i == self._value, "selected")

    def _select_next_option(self):
        n = len(self.options)
        self.options[self._value].remove_class("selected")
        self._value = (self._value + 1) % n
        self.options[self._value].add_class("selected")

    def _select_prev_option(self):
        n = len(self.options)
        self.options[self._value].remove_class("selected")
        self._value = (self._value - 1 + n) % n
        self.options[self._value].add_class("selected")

    def compose(self) -> ComposeResult:
        for option in self.options:
            yield option


class NumberScroll(BaseOption):
    def __init__(self, setting_name: str):
        super().__init__(setting_name)
        self._value = 0

    @property
    def value(self):
        return self._value

    def _select_next_option(self):
        self._value = min(self._value + 1, 100)
        self.refresh()

    def _select_prev_option(self):
        self._value = max(self._value - 1, 0)
        self.refresh()

    def render(self) -> RenderableType:
        return str(self._value)
