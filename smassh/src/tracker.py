from dataclasses import dataclass
from typing import Callable, Optional
from smassh.src.parser import config_parser
from .stats_tracker import StatsTracker, CheckPoint, Match

TrackerFunc = Callable[..., Optional["Cursor"]]


def force_correct(func: TrackerFunc) -> TrackerFunc:
    def wrapper(tracker: "Tracker", key: str) -> Optional[Cursor]:
        setting = config_parser.get("force_correct") == "on"
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


def difficulty(func: TrackerFunc) -> TrackerFunc:
    def wrapper(tracker: "Tracker", key: str) -> Optional[Cursor]:
        setting = config_parser.get("difficulty")

        if setting == "master" and tracker.paragraph[tracker.cursor_pos] != key:
            return

        if (
            setting == "expert"
            and tracker.paragraph[tracker.cursor_pos] == " "
            and tracker.stats.last_word_accuracy < 100
        ):
            return

        return func(tracker, key)

    return wrapper


@dataclass
class Cursor:
    """
    Cursor class to maintain record of checkpoints
    """

    old: int
    new: int
    correct: bool
    letter: str = ""

    def to_checkpoint(self) -> CheckPoint:
        if self.new > self.old:
            return CheckPoint(
                self.letter, self.new, Match.MATCH if self.correct else Match.MISMATCH
            )

        return CheckPoint(self.letter, self.new, Match.BACKSPACE)


class Tracker:
    """
    Tracker class to track keypresses on typing test
    """

    def __init__(self, paragraph: str) -> None:
        self.reset(paragraph)

    def reset(self, paragraph: str) -> None:
        self.paragraph = paragraph
        self.stats = StatsTracker()
        self.cursor_pos = 0

    def keypress(self, key: str) -> Optional[Cursor]:
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

    @difficulty
    @force_correct
    def handle_letter(self, key: str) -> Optional[Cursor]:
        if self.cursor_pos >= len(self.paragraph):
            return

        old = self.cursor_pos
        correct = key == self.paragraph[old]
        self.cursor_pos += 1
        return Cursor(old, self.cursor_pos, correct, self.paragraph[old])
