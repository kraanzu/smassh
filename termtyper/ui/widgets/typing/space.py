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
        self.current_key = None

    # ---------------- UTILS -----------------

    @property
    def cursor_row(self):
        return bisect_right(self.newlines, self.cursor)

    def reverse_span(self, pos: int) -> Span:
        return Span(pos, pos + 1, "reverse white")

    def cursor_span(self, correct: bool) -> Span:
        return Span(
            self.cursor - 1,
            self.cursor,
            "green" if correct else "red",
        )

    # ----------------- RENDER ------------------

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

    def update_cursor(self) -> None:
        self.paragraph.spans.append(self.reverse_span(self.cursor))

    def update_colors(self) -> None:
        if not self.current_key:
            return

        self.paragraph.spans.pop()
        key = self.current_key
        spans = self.paragraph.spans

        while spans and spans[-1].start >= self.cursor:
            spans.pop()

        if len(key) != 1:
            return

        # -1 because the cursor is ahead if a key is pressed
        correct = self.paragraph.plain[self.cursor - 1] == key
        self.paragraph.spans.append(self.cursor_span(correct))

    # ---------------- KEYPRESS -----------------

    def apply_key(self, key: str) -> None:
        if key == "backspace":
            self.cursor -= 1
            return

        self.cursor += 1

    def keypress(self, key: str) -> None:

        if key == "space":
            key = " "

        current_row = self.cursor_row
        self.current_key = key

        if (
            self.cursor_row != current_row
            and self.cursor_row > 1
            and isinstance(self.parent, Widget)
        ):
            self.parent.scroll_down()

        self.apply_key(key)
        self.update_colors()
        self.update_cursor()

        self.refresh()
