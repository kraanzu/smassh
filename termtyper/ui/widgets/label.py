from typing import Optional
from rich.console import RenderableType
from textual.widget import Widget
from termtyper.src.figlet import generate_figlet
from termtyper.ui.events import SetScreen


class NavItemBase(Widget):
    DEFAULT_CSS = """
    NavItemBase {
        content-align: center middle;
        width: auto;
        padding: 1;
    }
    """

    def __init__(self, text: str, screen_name: Optional[str] = None):
        super().__init__()
        self.text = text
        self.screen_name = screen_name

    def on_click(self) -> None:
        if self.screen_name:
            self.post_message(SetScreen(self.screen_name))

    def render(self) -> RenderableType:
        return self.text


class Banner(NavItemBase):
    """
    Text Widget to render text in a bigger font
    """

    def render(self) -> RenderableType:
        return generate_figlet(self.text)


class NavItem(NavItemBase):
    """
    Just a label widget with a callback
    """

    def on_click(self) -> None:
        if self.parent:
            for item in self.parent.query(NavItem):
                item.remove_class("active")
            self.add_class("active")
