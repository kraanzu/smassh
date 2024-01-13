from bisect import bisect_right
from rich.console import RenderableType
from rich.text import Span, Text
from textual.widget import Widget
from termtyper.src import master_generator, Tracker, Cursor
from termtyper.src.buddy import Buddy
from termtyper.src.parser import config_parser
from termtyper.ui.events import ShowResults
from termtyper.ui.widgets.typing.ticker import Ticker


def cursor_buddy(func):
    def wrapper(space: "Space") -> RenderableType:
        wpm = config_parser.get("cursor_buddy_speed")
        res = func(space)

        if not wpm or not space.tracker.stats.start_time:
            return res

        elapsed = space.tracker.stats.elapsed_time
        letters_typed = Buddy.get_letters_typed(elapsed, wpm, 5)

        if letters_typed > len(space.paragraph.plain):
            return res

        res_copy = res.copy()
        style = space.get_component_rich_style("--cursor-buddy")
        res_copy.spans.append(Span(letters_typed, letters_typed + 1, style))
        return res_copy

    return wrapper


class Space(Widget):
    DEFAULT_CSS = """
    Space {
        height: auto;
    }
    """

    COMPONENT_CLASSES = {
        "--cursor-buddy",
        "--correct-match",
        "--incorrect-match",
    }

    def __init__(self):
        super().__init__()
        self.current_key = None
        self.reset()
        self.check_timer = self.set_interval(1, self.check_restrictions, pause=True)
        if config_parser.get("cursor_buddy_speed"):
            self.set_interval(0.1, self.refresh)

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

    def check_restrictions(self):
        if not self.tracker.stats.start_time:
            return

        if min_speed := config_parser.get("min_speed"):
            wpm = self.tracker.stats.wpm
            if wpm < min_speed:
                return self.finish_typing()

        if min_accuracy := config_parser.get("min_accuracy"):
            accuracy = self.tracker.stats.accuracy
            if accuracy < min_accuracy:
                return self.finish_typing()

    def finish_typing(self):
        self.check_timer.pause()
        self.screen.query_one(Ticker).update_check.pause()
        self.screen.post_message(ShowResults(self.tracker.stats))

    def reset(self) -> None:
        generated = master_generator.generate(config_parser.get("language"))
        self.paragraph = Text(generated)
        self.reset_components()

    def reset_components(self) -> None:
        self.paragraph.spans.append(self.reverse_span(0))
        self.tracker = Tracker(self.paragraph.plain)
        self.cursor = 0

        if self.size.width:
            self.reset_newlines()
            self.screen.query_one(Ticker).reset()

        self.refresh()

    @cursor_buddy
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

        rich_style = "correct" if correct else "incorrect"
        style = self.get_component_rich_style(f"--{rich_style}-match")

        if diff == 1:
            span = Span(old, new, style)
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

        self.check_timer.resume()
        self.refresh()
