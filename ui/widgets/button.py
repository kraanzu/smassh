from rich.align import Align
from rich.box import SIMPLE
from rich.style import StyleType
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.message import Message
from textual.widget import Widget


class ButtonClicked(Message, bubble=True):
    pass


class Button(Widget):
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

    def on_enter(self):
        self.is_hover = True
        self.refresh()

    def on_leave(self):
        self.is_hover = False
        self.refresh()

    async def on_click(self, _: events.Click) -> None:
        await self.emit(ButtonClicked(self))

    def render(self):
        return Panel(Align.center(self.render_button(), vertical="middle"), box=SIMPLE)

    def render_button(self):
        return Panel(
            Align.center(
                Text(self.label, style=self.bt_style),
                vertical="middle",
            ),
            style="black",
            border_style=self.bt_border_style if not self.is_hover else "bold magenta",
            # box=ROUNDED if not self.is_hover else HEAVY_EDGE,
            expand=False,
            height=5,
        )
