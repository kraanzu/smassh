from textual import events
from textual.widget import Widget
from rich.text import Text


class NumberScroll(Widget):
    def __init__(
        self,
        name: str,
        start: int = 0,
        step: int = 1,
        min_value: int = 0,
        max_value: int = 500,
    ):
        super().__init__()
        self.name = name
        self.value = start
        self.step = step
        self.max_value = max_value
        self.min_value = min_value

    def on_mouse_scroll_down(self, _: events.MouseScrollDown):
        self.value = min(self.step + self.value, self.max_value)
        self.refresh()

    def on_mouse_scroll_up(self, _: events.MouseScrollUp):
        self.value = max(self.value - self.step, self.min_value)
        self.refresh()

    def render(self):
        return Text(str(self.value).center(5), style="reverse green")


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(NumberScroll("test", 1))

    MyApp.run()
