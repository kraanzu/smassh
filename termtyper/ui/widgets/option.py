from typing import List
from rich.console import RenderableType
from textual.widget import Widget


class BaseOption(Widget):
    def __init__(self, setting_name: str):
        super().__init__()

    def highlight(self):
        pass

    def lowlight(self):
        pass

    def select_next_option(self):
        pass

    def select_prev_option(self):
        pass

    def render(self) -> RenderableType:
        return "HIIII"


class Option(BaseOption):
    def __init__(self, setting_name: str, options: List[str]):
        super().__init__(setting_name)
        self.options = options


class NumberScroll(BaseOption):
    def __init__(self, setting_name: str):
        super().__init__(setting_name)
