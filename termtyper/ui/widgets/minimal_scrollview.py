from rich.console import RenderableType
from textual.layouts.grid import GridLayout
from textual.message import Message
from textual.widgets import ScrollView


class MinimalScrollView(ScrollView):
    """
    Just a ScrollView without bars
    """

    async def update(self, renderable: RenderableType, home: bool = False) -> None:
        return await super().update(renderable, home)

    def scroll_down(self) -> None:
        return

    def scroll_up(self) -> None:
        return

    def upscroll(self):
        super().scroll_up()

    def downscroll(self):
        super().scroll_down()

    async def handle_window_change(self, message: Message) -> None:
        message.stop()

        virtual_width, virtual_height = self.window.virtual_size
        width, height = self.size

        self.x = self.validate_x(self.x)
        self.y = self.validate_y(self.y)

        self.hscroll.virtual_size = virtual_width
        self.hscroll.window_size = width
        self.vscroll.virtual_size = virtual_height
        self.vscroll.window_size = height

        assert isinstance(self.layout, GridLayout)
