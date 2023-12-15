from bisect import bisect_left
import textwrap
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget
from termtyper.src.generator import master_generator


class Space(Widget):
    def __init__(self):
        super().__init__()
        self.reset()

    @property
    def cursor_row(self):
        return bisect_left(self.newlines, self.cursor)

    def on_show(self):
        paragraph = self.paragraph.plain
        width = self.size.width
        lines = textwrap.wrap(paragraph, width)
        self.newlines = [len(line) for line in lines]

    def reset(self) -> None:
        generated = master_generator.generate()
        self.paragraph = Text(generated)
        self.cursor = 0

    def render(self) -> RenderableType:
        return self.paragraph
