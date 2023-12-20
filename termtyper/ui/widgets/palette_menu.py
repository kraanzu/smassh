from typing import Callable, List, Optional
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input


class PaletteMenu(Widget):
    DEFAULT_CSS = """
    PaletteMenu {
    }
    """

    def __init__(self, callback: Optional[Callable] = None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.options = self.get_options()

    def get_options(self) -> List[str]:
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        yield Input()


class LanguagePaletteMenu(PaletteMenu):
    def __init__(self):
        super().__init__()

    def get_options(self) -> List[str]:
        return ["english", "french"]


class ThemePaletteMenu(PaletteMenu):
    def __init__(self):
        super().__init__()

    def get_options(self) -> List[str]:
        return ["nord", "catapuccin"]
