from rich.align import Align
from rich.box import SIMPLE
from rich.console import RenderableType
from rich.style import StyleType
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.message import Message
from textual.widget import Widget


class ButtonSelect(Message, bubble=True):
    """
    An Event class for when the Button is clicked
    """

    pass


class ButtonClicked(Message, bubble=True):
    """
    An Event class for when the Button is clicked
    """

    pass


class Button(Widget):
    """
    A class that renders a panel acting like a button
    """

    def __init__(
        self,
        name: str | None = None,
        label: str = "Click Me !",
        style: StyleType = "bold blue",
        border_style: StyleType = "dim white",
    ) -> None:
        super().__init__(name)
        self.label = label
        self.bt_style = style
        self.bt_border_style = border_style
        self.is_hover = False

    def select(self):
        self.is_hover = True
        self.refresh()

    def deselect(self):
        self.is_hover = False
        self.refresh()

    async def on_enter(self) -> None:
        """
        called when hovered by mouse pointer
        """
        await self.emit(ButtonSelect(self))

    # def on_leave(self) -> None:
    #     """
    #     called when the mouse pointer leaves
    #     """
    #     self.is_hover = False
    #     self.refresh()

    async def on_click(self, _: events.Click) -> None:
        await self.emit(ButtonClicked(self))

    def render(self) -> RenderableType:
        """
        Wraps the button in a Panel with no borders for proper layout
        """

        return Panel(Align.center(self.render_button(), vertical="middle"), box=SIMPLE)

    def render_button(self) -> RenderableType:
        return Panel(
            Align.center(
                Text(self.label, style=self.bt_style),
                vertical="middle",
            ),
            style="black",
            border_style=self.bt_border_style if not self.is_hover else "bold magenta",
            expand=False,
            height=5,
        )
