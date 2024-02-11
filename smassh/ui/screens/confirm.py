from typing import Literal
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Static


class ConfirmButton(Widget):
    def __init__(
        self, label: str, button_type: Literal["ok", "cancel"], *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.label = label
        self.button_type = button_type

    def render(self) -> RenderableType:
        return self.label


class MessageDialogue(Widget):

    DEFAULT_CSS = """
    MessageDialogue {
        layout: grid;
        width: 50;
        height: 4;
        background: black;
        grid-size: 2 2;
        grid-rows: 3 1;
        grid-columns: 1fr 1fr;
    }

    MessageDialogue > Static {
        column-span: 2;
        height: 100%;
        background: orange;
    }

    MessageDialogue > ConfirmButton {
        background: blue;
    }
    """

    def __init__(self, message: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(self.message)
        yield ConfirmButton("OK", button_type="ok")
        yield ConfirmButton("CANCEL", button_type="cancel")


class ConfirmScreen(Screen):
    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield MessageDialogue("Are you sure?")
