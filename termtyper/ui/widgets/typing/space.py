from bisect import bisect_right
from rich.console import RenderableType
from rich.text import Span, Text
from textual.widget import Widget
from termtyper.src import master_generator, Tracker, Cursor
from termtyper.src.parser import config_parser
from termtyper.ui.events import ShowResults


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

    def cursor_row(self, cursor_pos: int) -> int:
        return bisect_right(self.newlines, cursor_pos)

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
        self.reset_newlines()

    def reset_newlines(self) -> None:
        self.newlines = master_generator.get_newlines(
            self.paragraph.plain,
            self.size.width,
        )

    def restart(self) -> None:
        if config_parser.get("restart_same"):
            generated = self.paragraph.plain
            self.paragraph = Text(generated)
            self.reset_components()
        else:
            self.reset()

    def reset(self) -> None:
        generated = master_generator.generate()
        self.paragraph = Text(generated)

    def reset_components(self) -> None:
        self.paragraph.spans.append(self.reverse_span(0))
        self.tracker = Tracker(self.paragraph.plain, intervention=self.intervene)
        self.cursor = 0
        self.refresh()

        if self.size.width:
            self.reset_newlines()

    def intervene(self, message: str):
        ...

    def render(self) -> RenderableType:
        return self.paragraph

    def update_colors(self, cursor: Cursor) -> None:
        self.paragraph.spans.pop()
        old = cursor.old
        new = cursor.new
        correct = cursor.correct

        if new < old:
            self.paragraph.spans = self.paragraph.spans[:new]
            return

        diff = new - old

        empty_spans = [Span(i, i + 1, "") for i in range(old, new - 1)]
        self.paragraph.spans.extend(empty_spans)
        if diff == 1:
            span = Span(old, new, "green" if correct else "red")
            self.paragraph.spans.append(span)
            return

    # ---------------- KEYPRESS -----------------

    def keypress(self, key: str) -> None:
        cursor = self.tracker.keypress(key)
        if not cursor:
            return

        current_row = self.cursor_row(cursor.old)
        new_row = self.cursor_row(cursor.new)

        if current_row != new_row and isinstance(self.parent, Widget):
            if new_row > current_row:
                if current_row:
                    self.parent.scroll_down()
            else:
                if current_row != len(self.newlines) - 1:
                    self.parent.scroll_up()

        self.update_colors(cursor)
        self.paragraph.spans.append(self.reverse_span(cursor.new))

        if cursor.new == len(self.paragraph.plain):
            self.screen.post_message(ShowResults(self.tracker.stats))

        self.refresh()
