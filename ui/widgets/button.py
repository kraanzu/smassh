from rich.align import Align
from rich.style import Style, StyleType
from rich.panel import Panel
from rich.text import Text
from textual.widget import Widget


class Button(Widget):
    def __init__(
        self,
        name: str | None = None,
        label: str = "Click Me !",
        style: StyleType = "bold blue",
        border_style: StyleType = "bold magenta",
    ) -> None:
        super().__init__(name)
        self.label = label
        self.bt_style = style
        self.bt_border_style = border_style

    def render(self):
        return Panel(
            Align.center(Text(self.label, style=self.bt_style)),
            style="black",
            border_style=self.bt_border_style,
            expand=False,
            height=3,
            width=15,
        )
