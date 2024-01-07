from dataclasses import dataclass
from typing import Optional


@dataclass
class Cursor:
    old: int
    new: int
    correct: bool


class Tracker:
    def __init__(self, paragraph: str) -> None:
        self.reset(paragraph)

    def reset(self, paragraph: str) -> None:
        self.paragraph = paragraph
        self.cursor_pos = 0

    def keypress(self, key: str) -> Optional[Cursor]:
        if key == "space":
            key = " "

        if key == "backspace":
            return self.handle_delete_letter()

        if key == "ctrl+w":
            return self.handle_delete_word()

        if len(key) == 1:
            return self.handle_letter(key)

    def handle_delete_letter(self) -> Optional[Cursor]:
        old = self.cursor_pos

        if self.cursor_pos == 0:
            return

        self.cursor_pos -= 1
        return Cursor(old, self.cursor_pos, True)

    def handle_delete_word(self) -> Cursor:
        ...

    def handle_letter(self, key: str) -> Cursor:
        old = self.cursor_pos

        if key == self.paragraph[self.cursor_pos]:
            self.cursor_pos += 1
            return Cursor(old, self.cursor_pos, True)

        self.cursor_pos += 1
        return Cursor(old, self.cursor_pos, False)
