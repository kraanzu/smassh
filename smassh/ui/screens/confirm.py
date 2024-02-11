from typing import Literal
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget


class ConfirmButton(Widget):
    DEFAULT_CSS = """
    ConfirmButton {
        padding: 1;
        height: 3;
        content-align: center middle;
    }
    """

    def __init__(
        self,
        label: str,
        button_type: Literal["ok", "cancel"],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.label = label
        self.button_type = button_type

    def render(self) -> RenderableType:
        return self.label


class MessageBox(Widget):
    DEFAULT_CSS = """
    MessageBox {
        content-align: center middle;
        column-span: 2;
    }
    """

    def render(self) -> RenderableType:
        return "Are you sure?\nThis action cannot be undone."


class MessageDialogue(Widget):

    DEFAULT_CSS = """
    MessageDialogue {
        layout: grid;
        width: 50;
        height: auto;
        background: black;
        grid-size: 2 2;
        grid-rows: 4 3;
        grid-columns: 1fr 1fr;
        border: solid red;
    }
    """

    def compose(self) -> ComposeResult:
        yield MessageBox()
        yield ConfirmButton("OK", button_type="ok")
        yield ConfirmButton("CANCEL", button_type="cancel")


class ConfirmScreen(Screen):
    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield MessageDialogue()
