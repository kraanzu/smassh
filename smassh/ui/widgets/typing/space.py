from bisect import bisect_right
from typing import List
from rich.console import RenderableType
from rich.style import Style
from rich.text import Span, Text
from textual.widget import Widget
from textual.widgets import Static
from smassh.src import master_generator, Tracker, Cursor
from smassh.src.buddy import Buddy
from smassh.src.parser import config_parser
from smassh.ui.events import ShowResults
from smassh.ui.widgets.typing.ticker import Ticker


def caret(func):
    def wrapper(space: "Space") -> Text:
        renderable: Text = func(space).copy()
        setting = config_parser.get("caret_style")
        pos = space.tracker.cursor_pos

        if setting == "off" or pos == len(space.paragraph.plain):
            return renderable

        if setting == "underline":
            rich_style = "--caret-underline"
        else:
            rich_style = "--caret-block"

        style = space.get_component_rich_style(rich_style)
        renderable.spans.append(Span(pos, pos + 1, style))

        return renderable

    return wrapper


def tab_reset(func):
    def wrapper(space: "Space", key: str) -> None:
        if key == "tab" and config_parser.get("tab_reset"):
            return space.restart()

        return func(space, key)

    return wrapper


def toggle_settings(func):
    def wrapper(space: "Space", key: str) -> None:
        config_changed = False

        if key == "ctrl+n":
            config_parser.toggle_numbers()
            config_changed = True

        elif key == "ctrl+p":
            config_parser.toggle_punctuations()
            config_changed = True

        if config_changed:
            for i in space.screen.query("Switchable"):
                i.refresh()

            return space.restart()

        return func(space, key)

    return wrapper


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


def blind_mode(func):
    def wrapper(space: "Space", *args, **kwargs) -> Style:
        if config_parser.get("blind_mode"):
            return space.get_component_rich_style("--blind-match")

        return func(space, *args, **kwargs)

    return wrapper


class Space(Static):
    """
    Space Widget to handle keypress and display typing text
    """

    COMPONENT_CLASSES = {
        "--cursor-buddy",
        "--correct-match",
        "--incorrect-match",
        "--blind-match",
        "--caret-underline",
        "--caret-block",
    }

    def __init__(self) -> None:
        super().__init__()
        self.current_key = None
        self.reset()
        self.check_timer = self.set_interval(1, self.check_restrictions, pause=True)
        if config_parser.get("cursor_buddy_speed"):
            self.set_interval(0.1, self.refresh)

    # ---------------- UTILS -----------------

    def cursor_row(self, cursor_pos: int) -> int:
        return bisect_right(self.newlines, cursor_pos)

    def cursor_span(self, pos: int) -> Span:
        return Span(pos, pos + 1, "reverse white")

    # ----------------- RENDER ------------------
    def on_show(self) -> None:
        self.reset_newlines()

    def reset_newlines(self) -> None:
        self.newlines = master_generator.get_newlines(
            self.paragraph.plain,
            self.size.width,
        )

    def restart(self, force: bool = False) -> None:
        if force:
            generated = self.paragraph.plain
            self.paragraph = Text(generated)
            self.reset_components()
        else:
            self.reset()

    def check_restrictions(self) -> None:
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

        if min_burst := config_parser.get("min_burst"):
            burst = self.tracker.stats.last_word_wpm
            if burst < min_burst:
                return self.finish_typing()

    def finish_typing(self, fail: bool = True) -> None:
        self.screen.post_message(ShowResults(self.tracker.stats, fail))

    def reset(self) -> None:
        mode = config_parser.get("mode")
        if mode == "words":
            word_count = config_parser.get(f"{mode}_count")
        else:
            minutes = config_parser.get(f"{mode}_count") / 60
            word_count = round(600 * minutes)

        language = config_parser.get("language")

        generated = master_generator.generate(
            language,
            word_count,
        )

        self.paragraph = Text(generated)
        self.reset_components()

    def reset_components(self) -> None:
        self.tracker = Tracker(self.paragraph.plain)
        self.cursor = 0
        self.paragraph_spans = []

        if self.size.width:
            self.reset_newlines()
            self.screen.query_one(Ticker).reset()

        self.refresh(layout=True)

    @cursor_buddy
    @caret
    def render(self) -> RenderableType:
        self.paragraph.spans = self.get_colorized()
        return self.paragraph

    @blind_mode
    def get_match_style(self, correct: bool) -> Style:
        rich_style = "correct" if correct else "incorrect"
        style = self.get_component_rich_style(f"--{rich_style}-match")
        return style

    def get_colorized(self) -> List[Span]:
        spans = []
        for index, keymatch in enumerate(self.paragraph_spans):
            if keymatch != "":
                spans.append(
                    Span(
                        index,
                        index + 1,
                        self.get_match_style(keymatch),
                    )
                )
            else:
                spans.append(
                    Span(
                        index,
                        index + 1,
                        "",
                    )
                )

        return spans

    def update_colors(self, cursor: Cursor) -> None:
        old = cursor.old
        new = cursor.new
        correct = cursor.correct

        if new < old:
            self.paragraph.spans = self.paragraph.spans[:new]
            return

        diff = new - old
        self.paragraph_spans.extend([""] * (diff - 1))

        if diff == 1:
            self.paragraph_spans.append(correct)

    # ---------------- KEYPRESS -----------------

    @toggle_settings
    @tab_reset
    def keypress(self, key: str) -> None:
        if key == "escape":
            return self.reset()

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
        if cursor.new == len(self.paragraph.plain):
            return self.finish_typing(fail=False)

        self.check_timer.resume()
        self.screen.query_one(Ticker).update_check.resume()
        self.refresh()
