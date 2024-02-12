from typing import Literal
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.binding import Binding
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
        classes = "ok-btn" if button_type == "ok" else "cancel-btn"
        super().__init__(classes=classes, *args, **kwargs)
        self.label = label
        self.button_type = button_type

    def on_click(self) -> None:
        return self.dismiss()

    def dismiss(self) -> None:
        return self.screen.dismiss(self.button_type == "ok")

    def render(self) -> RenderableType:
        return self.label


class MessageBox(Widget):
    DEFAULT_CSS = """
    MessageBox {
        content-align: center middle;
        column-span: 2;
        text-style: bold italic;
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
        self.ok = ConfirmButton("[O]K", button_type="ok")
        self.cancel = ConfirmButton("[C]ANCEL", button_type="cancel")

        yield MessageBox()
        yield self.ok
        yield self.cancel


class ConfirmScreen(Screen):
    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }
    """

    BINDINGS = [
        Binding("escape", "app.pop_screen"),
    ]

    def compose(self) -> ComposeResult:
        yield MessageDialogue()

    def key_o(self):
        self.query_one(MessageDialogue).ok.dismiss()

    def key_c(self):
        self.query_one(MessageDialogue).cancel.dismiss()
