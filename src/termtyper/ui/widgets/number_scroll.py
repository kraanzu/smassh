from rich.align import Align
from rich.console import RenderableType
from textual import events
from textual.widget import Widget
from rich.text import Text
from rich.panel import Panel

from ...utils import Parser


class NumberScroll(Widget):
    """
    A number scroll that acts as an option to set a particular value
    """

    def __init__(
        self,
        name: str,
        step: int = 1,
        min_value: int = 0,
        max_value: int = 500,
    ) -> None:
        super().__init__()
        self.name = name
        self.value = int(Parser().get_data(self.name))
        self.step = step
        self.max_value = max_value
        self.min_value = min_value
        self.selected = False

    def highlight(self):
        self.selected = True
        self.refresh()

    def lowlight(self):
        self.selected = False
        self.refresh()

    def update(self):
        Parser().set_data(self.name, str(self.value))
        self.refresh()

    def select_next_option(self) -> None:
        self.value = min(self.step + self.value, self.max_value)
        self.update()

    def select_prev_option(self) -> None:
        self.value = max(self.value - self.step, self.min_value)
        self.update()

    def on_mouse_scroll_down(self, _: events.MouseScrollDown) -> None:
        self.select_next_option()

    def on_mouse_scroll_up(self, _: events.MouseScrollUp) -> None:
        self.select_prev_option()

    def render(self) -> RenderableType:
        return Panel(
            Align.center(
                Text(str(self.value).center(5), style="reverse green"),
                vertical="middle",
            ),
            border_style="magenta" if self.selected else "white",
        )


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(NumberScroll("test", 1))

    MyApp.run()