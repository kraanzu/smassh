import operator
import textwrap
from bisect import bisect_right
from itertools import accumulate
from rich.console import RenderableType
from rich.text import Span, Text
from textual.widget import Widget
from termtyper.src.generator import master_generator


class Space(Widget):
    DEFAULT_CSS = """
    Space {
        height: auto;
    }
    """

    def __init__(self):
        super().__init__()
        self.reset()

    @property
    def cursor_row(self):
        return bisect_right(self.newlines, self.cursor)

    def reverse_span(self, pos: int) -> Span:
        return Span(pos, pos + 1, "reverse")

    def on_show(self):
        paragraph = self.paragraph.plain
        width = self.size.width
        lines = textwrap.wrap(paragraph, width)
        self.newlines = list(
            accumulate(
                [len(line) + 1 for line in lines],
                operator.add,
            )
        )

    def reset(self) -> None:
        generated = master_generator.generate()
        self.paragraph = Text(generated)
        self.paragraph.spans.append(self.reverse_span(0))
        self.cursor = 0

    def render(self) -> RenderableType:
        return self.paragraph

    def update_colors(self, key: str) -> None:
        correct = self.paragraph.plain[self.cursor] == key
        self.paragraph.spans.append(
            Span(
                self.cursor,
                self.cursor + 1,
                "green" if correct else "red",
            )
        )
        self.paragraph.spans.append(self.reverse_span(self.cursor + 1))

    def keypress(self, key: str) -> None:
        self.paragraph.spans.pop()
        current_row = self.cursor_row
        self.update_colors(key)
        self.cursor += 1
        if self.cursor_row != current_row and self.cursor_row > 1:
            self.parent.scroll_down()

        self.refresh()
