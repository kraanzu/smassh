from typing import Literal, Optional
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget


class StripSetting(Widget):
    DEFAULT_CSS = """
    StripSetting {
        width: auto;
        height: 1;
        padding: 0 1;
    }
    """

    def __init__(self, setting_name: str, icon: Optional[str] = None):
        super().__init__()
        self.setting_name = setting_name
        self.icon = icon

    def render(self) -> RenderableType:

        if self.icon:
            return self.icon + " " + self.setting_name

        return self.setting_name


class StripSeparator(Widget):

    DEFAULT_CSS = """
    StripSeparator {
        width: auto;
        height: 1;
    }
    """

    def __init__(self):
        super().__init__(disabled=True)

    def render(self) -> RenderableType:
        return " | "


class Bracket(Widget):
    DEFAULT_CSS = """
    Bracket {
        width: auto;
        height: 1;
    }
    """

    def __init__(self, bracket_type: Literal["left", "right"]):
        super().__init__(disabled=True)
        self.bracket_type = bracket_type

    def render(self) -> RenderableType:
        if self.bracket_type == "left":
            return ""
        else:
            return ""


class TypingConfigStrip(Widget):
    DEFAULT_CSS = """
    TypingConfigStrip {
        column-span: 3;
        layout: horizontal;
        height: 3;
        align: center middle;
        padding: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Bracket("left")
        yield StripSetting("punctuation", "󰸥")
        yield StripSetting("numbers", "󰲰")
        yield StripSeparator()
        yield StripSetting("time", "󰥔")
        yield StripSetting("words", "󰯬")
        yield StripSeparator()
        yield StripSetting("15")
        yield StripSetting("30")
        yield StripSetting("60")
        yield StripSetting("120")
        yield Bracket("right")
