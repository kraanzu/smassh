from typing import Literal, Optional
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget
from smassh.src import config_parser
from smassh.ui.widgets.typing.space import Space


class StripSetting(Widget):
    """
    Single setting widget for strip in the typing screen
    """

    DEFAULT_CSS = """
    StripSetting {
        width: auto;
        height: 1;
        padding: 0 1;
    }
    """

    def __init__(self, setting_name: str, icon: Optional[str] = None) -> None:
        super().__init__()
        self.setting_name = setting_name
        self.icon = icon
        self.shrink = False

    def render(self) -> RenderableType:
        if self.icon:
            return self.icon + " " + self.setting_name

        return self.setting_name


class Switchable(StripSetting):
    """
    A toggle-able setting for typing strip
    """

    setting_name: str
    setting_icon: str

    def __init__(self) -> None:
        super().__init__(self.setting_name, self.setting_icon)
        self.refresh_setting()

    def refresh_setting(self) -> None:
        self.set_class(config_parser.get(self.setting_name), "enabled")

    def _toggle(self) -> None: ...

    def toggle(self) -> None:
        self._toggle()
        self.refresh_setting()

    def on_click(self) -> None:
        self.toggle()
        self.screen.query_one(Space).reset()

    def render(self) -> RenderableType:
        self.refresh_setting()
        return super().render()


class PunctuationSwitch(Switchable):
    setting_name = "punctuations"
    setting_icon = "󰸥"

    def _toggle(self) -> None:
        config_parser.toggle_punctuations()


class NumberSwitch(Switchable):
    setting_name = "numbers"
    setting_icon = "󰲰"

    def _toggle(self) -> None:
        config_parser.toggle_numbers()


class WordMode(Switchable):
    setting_name = "words"
    setting_icon = "󰯬"

    def _refresh_mode_count(self) -> None:
        for counts in self.screen.query(ModeCount):
            counts.refresh()

    def _toggle(self) -> None:
        config_parser.toggle_mode()
        self._refresh_mode_count()
        self.screen.query_one(TimeMode).refresh_setting()

    def refresh_setting(self) -> None:
        configured_mode = config_parser.get("mode")
        self.set_class(configured_mode == "words", "enabled")


class TimeMode(Switchable):
    setting_name = "time"
    setting_icon = "󰥔"

    def _refresh_mode_count(self) -> None:
        for counts in self.screen.query(ModeCount):
            counts.refresh()

    def _toggle(self) -> None:
        config_parser.toggle_mode()
        self._refresh_mode_count()
        self.screen.query_one(WordMode).refresh_setting()

    def refresh_setting(self) -> None:
        configured_mode = config_parser.get("mode")
        self.set_class(configured_mode == "time", "enabled")


class ModeCount(Widget):
    DEFAULT_CSS = """
    ModeCount {
        width: auto;
    }
    """

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value
        self.shrink = False

    def _refresh_other_counts(self) -> None:
        for counts in self.screen.query(ModeCount):
            counts.refresh()

    def on_click(self) -> None:
        config_parser.set(f"{config_parser.get('mode')}_count", self.value)
        self._refresh_other_counts()
        self.screen.query_one(Space).reset()

    def render(self) -> RenderableType:
        mode = config_parser.get("mode")
        count = config_parser.get(f"{mode}_count")
        self.set_class(count == self.value, "enabled")
        return str(self.value) + " "


class StripSeparator(Widget):
    DEFAULT_CSS = """
    StripSeparator {
        width: auto;
        height: 1;
    }
    """

    def __init__(self) -> None:
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

    def __init__(self, bracket_type: Literal["left", "right"]) -> None:
        super().__init__(disabled=True)
        self.bracket_type = bracket_type

    def render(self) -> RenderableType:
        if self.bracket_type == "left":
            return ""
        else:
            return ""


class StripSection(Widget):
    DEFAULT_CSS = """
    StripSection {
        layout: horizontal;
        width: auto;
        height: 1;
    }
    """


class LeftStripSection(StripSection): ...


class MiddleStripSection(StripSection): ...


class RightStripSection(StripSection): ...


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

        with LeftStripSection():
            yield PunctuationSwitch()
            yield NumberSwitch()

        yield StripSeparator()

        with MiddleStripSection():
            yield WordMode()
            yield TimeMode()

        yield StripSeparator()

        with RightStripSection():
            for i in [15, 30, 60, 120]:
                yield ModeCount(i)

        yield Bracket("right")
