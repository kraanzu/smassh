from typing import Literal
from bisect import bisect

from rich.text import Span, Text
from rich.panel import Panel
from textual.app import App
from textual.widget import Widget
from textual.message import Message, MessageTarget


class FinishedTyping(Message, bubble=True):
    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


class Screen(Widget):
    def __init__(
        self,
        paragraph: str,
        speed_threshold: int = 0,
        accuracy_threshhold: int = 0,
        min_burst: int = 0,
        cursor_buddy_speed: int | None = None,
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
        self.paragraph = Text(paragraph, spans=[Span(0, 0, "magenta")])
        self.paragraph.append(" " + str(self._size))

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
        self.total_key_presses = 0
        self.mistakes = 0
        self.mistakes_hashmap = dict()

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
                    self.cursor_position = self.spaces[
                        bisect(self.spaces, self.cursor_position)
                    ]

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
                + [Span(self.cursor_position, self.cursor_position + 1, "reverse")],
            )
        )


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.x = Screen("hi")
            await self.view.dock(self.x)

    MyApp.run()
