from bisect import bisect_left
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget
from termtyper.src.generator import master_generator


class Space(Widget):
    DEFAULT_CSS = """
    Space {
        height: 100%;
        width: 100%;
        content-align: center middle;
    }
    """

    def __init__(self):
        super().__init__()
        self.reset()

    @property
    def cursor_row(self):
        return bisect_left(self.newlines, self.cursor)

    def reset(self) -> None:
        generated = master_generator.generate()
        self.newlines = [index for index, i in enumerate(generated) if i == "\n"]
        self.paragraph = Text(generated)
        self.cursor = 0

    def render(self) -> RenderableType:
        return self.paragraph
