from typing import List
from rich.console import RenderableType
from textual.widget import Widget


class BaseOption(Widget):
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

    def select_next_option(self):
        pass

    def select_prev_option(self):
        pass


class Option(BaseOption):
    def __init__(self, setting_name: str, options: List[str]):
        super().__init__(setting_name)
        self.options = options
        self._value = 0

    @property
    def value(self):
        return self.options[self._value]


class NumberScroll(BaseOption):
    def __init__(self, setting_name: str):
        super().__init__(setting_name)
        self._value = 0

    @property
    def value(self):
        return self._value

    def select_next_option(self):
        self._value = min(self._value + 1, 100)
        self.refresh()

    def select_prev_option(self):
        self._value = max(self._value - 1, 0)
        self.refresh()

    def render(self) -> RenderableType:
        return str(self._value)
