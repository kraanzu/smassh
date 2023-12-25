from typing import Callable, List, Optional
from textual.app import ComposeResult
from textual.widget import Widget
from .palette_input import PaletteInput
from .palette_list import PaletteList


class PaletteMenu(Widget):
    def __init__(self, callback: Optional[Callable] = None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.options = self.get_options()

    def get_options(self) -> List[str]:
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        yield PaletteInput()
        yield PaletteList()


class LanguagePaletteMenu(PaletteMenu):
    def get_options(self) -> List[str]:
        return ["english", "french"]


class ThemePaletteMenu(PaletteMenu):
    def get_options(self) -> List[str]:
        return ["nord", "catapuccin"]
