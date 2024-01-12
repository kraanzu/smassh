from dataclasses import dataclass
from typing import Any, Callable, Optional
from termtyper.src.parser import config_parser
from .stats_tracker import StatsTracker, CheckPoint, Match

TrackerFunc = Callable[["Tracker", Any], Optional["Cursor"]]


def force_correct(func: TrackerFunc) -> TrackerFunc:
    def wrapper(tracker: "Tracker", key: str) -> Optional[Cursor]:
        setting = config_parser.get("force_correct")
        if not setting or tracker.paragraph[tracker.cursor_pos] == key:
            return func(tracker, key)

    return wrapper


def confidence_mode(func: TrackerFunc) -> TrackerFunc:
    def wrapper(tracker: "Tracker", *args, **kwargs) -> Optional[Cursor]:
        setting = config_parser.get("confidence_mode")
        if setting == "max":
            return

        if (
            setting == "on"
            and tracker.cursor_pos
            and tracker.paragraph[tracker.cursor_pos - 1] == " "
        ):
            return

        result = func(tracker, *args, **kwargs)
        return result

    return wrapper


@dataclass
class Cursor:
    old: int
    new: int
    correct: bool

    def to_checkpoint(self) -> CheckPoint:
        if self.new > self.old:
            return CheckPoint(self.new, Match.MATCH if self.correct else Match.MISMATCH)

        return CheckPoint(self.new, Match.BACKSPACE)


class Tracker:
    def __init__(self, paragraph: str, intervention: Optional[Callable] = None) -> None:
        self.reset(paragraph)

        # callback function for cases where restrictions are broken
        self.intervention = intervention or (lambda _: None)

    def reset(self, paragraph: str) -> None:
        self.paragraph = paragraph
        self.stats = StatsTracker()
        self.cursor_pos = 0

    def keypress(self, key: str) -> Optional[Cursor]:
        if key == "space":
            key = " "

        res = None

        if key == "backspace":
            res = self.handle_delete_letter()

        elif key == "ctrl+w":
            res = self.handle_delete_word()

        elif len(key) == 1:
            res = self.handle_letter(key)

        if res:
            self.stats.add_checkpoint(res.to_checkpoint())
            return res

    @confidence_mode
    def handle_delete_letter(self) -> Optional[Cursor]:
        old = self.cursor_pos

        if self.cursor_pos == 0:
            return

        self.cursor_pos -= 1
        return Cursor(old, self.cursor_pos, True)

    @confidence_mode
    def handle_delete_word(self) -> Cursor:
        old = self.cursor_pos

        # incase it's the start of a word
        if self.cursor_pos:
            self.cursor_pos -= 1

        while self.cursor_pos > 0 and self.paragraph[self.cursor_pos - 1] != " ":
            self.cursor_pos -= 1

        return Cursor(old, self.cursor_pos, True)

    @force_correct
    def handle_letter(self, key: str) -> Cursor:
        old = self.cursor_pos

        if key == self.paragraph[self.cursor_pos]:
            self.cursor_pos += 1
            return Cursor(old, self.cursor_pos, True)

        self.cursor_pos += 1
        return Cursor(old, self.cursor_pos, False)
