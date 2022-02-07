from typing import Literal
from bisect import bisect
from os import get_terminal_size

from rich.text import Span, Text
from rich.panel import Panel
from textual.app import App
from textual.widget import Widget
from textual.message import Message, MessageTarget
from utils import chomsky, Parser


class FinishedTyping(Message, bubble=True):
    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


empty_span = Span(0, 0, "")


class Screen(Widget):
    def __init__(
        self,
        speed_threshold: int = 0,
        accuracy_threshhold: int = 0,
        min_burst: int = 0,
        cursor_buddy_speed: int = 190,
        force_correct: bool = False,
        tab_reset: bool = False,
        difficulty: Literal["normal", "expert", "master"] = "normal",
        restart_same: bool = False,
        blind_mode: bool = False,
        single_line_words: bool = False,
        sound: bool = False,
        caret_style: Literal["underline", "block", "off"] = "off",
    ):
        super().__init__()

        self.set_paragraph()
        self.speed_threshold = speed_threshold
        self.accuracy_threshhold = accuracy_threshhold
        self.min_burst = min_burst
        self.cursor_buddy_speed = cursor_buddy_speed
        self.force_correct = force_correct
        self.tab_reset = tab_reset
        self.difficulty = difficulty
        self.repeat_same = restart_same
        self.blind_mode = blind_mode
        self.single_line_words = single_line_words
        self.sound = sound
        self.caret_style = caret_style

        self.spaces = [i for i, j in enumerate(self.paragraph.plain) if j == " "] + [
            len(self.paragraph.plain)
        ]
        self.cursor_position = 0
        self.cursor_buddy_position = 0
        self.total_key_presses = 0
        self.mistakes = 0
        self.mistakes_hashmap = dict()

        if self.cursor_buddy_speed:
            self.set_interval(
                60 / (5 * self.cursor_buddy_speed), self.move_cursor_buddy
            )

    def move_cursor_buddy(self):
        if self.cursor_buddy_position < len(self.paragraph.plain) - 1:
            self.cursor_buddy_position += 1
            self.refresh()

    def reset_screen(self):
        self.cursor_position = 0
        if self.repeat_same:
            self.paragraph.spans = self.paragraph.spans[:1]
        else:
            self.set_paragraph()
        self.refresh()

    def set_paragraph(self):
        self.paragraph_size = Parser().get_data("paragraph_size")
        if self.paragraph_size == "teensy":
            times = 2
        elif self.paragraph_size == "small":
            times = 5
        elif self.paragraph_size == "big":
            times = 10
        else:
            times = 15

        paragraph = chomsky(times, get_terminal_size()[0] - 5)
        self.paragraph = Text(paragraph)
        self.refresh()

    def key_add(self, key: str):

        if key == "ctrl+i":  # TAB
            self.paragraph.spans = self.paragraph.spans[:1]
            self.cursor_position = 0

        elif key == "ctrl+h":  # BACKSPACE
            if self.cursor_position:
                self.cursor_position -= 1
                self.paragraph.spans.pop()

        elif len(key) == 1:
            if key == " ":
                if self.paragraph.plain[self.cursor_position] != " ":
                    next_space = self.spaces[bisect(self.spaces, self.cursor_position)]
                    self.paragraph.spans.extend(
                        [empty_span]
                        * (
                            next_space - self.cursor_position + 1
                        )  # 1 for the next space
                    )
                    self.cursor_position = next_space
                else:
                    self.paragraph.spans.append(empty_span)

            elif key == self.paragraph.plain[self.cursor_position]:
                self.paragraph.spans.append(
                    Span(self.cursor_position, self.cursor_position + 1, "green")
                )

            else:
                self.paragraph.spans.append(
                    Span(self.cursor_position, self.cursor_position + 1, "red")
                )

            self.cursor_position += 1

        self.refresh()

    def render(self):
        return Panel(
            Text(
                self.paragraph.plain,
                spans=self.paragraph.spans
                + [Span(self.cursor_position, self.cursor_position + 1, "reverse")]
                + [
                    Span(
                        self.cursor_buddy_position,
                        self.cursor_buddy_position + 1,
                        "reverse magenta",
                    )
                    if self.cursor_buddy_speed
                    else Span(0, 0, "")
                ],
            )
        )


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.x = Screen()
            await self.view.dock(self.x)

    MyApp.run()
