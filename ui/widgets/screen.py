import time
from bisect import bisect
from os import get_terminal_size
from rich.align import Align

from rich.text import Span, Text
from rich.panel import Panel
from textual.app import App
from textual.widget import Widget
from textual.message import Message, MessageTarget
from utils import chomsky, Parser


class FinishedTyping(Message, bubble=True):
    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


class UpdateRaceBar(Message, bubble=True):
    def __init__(self, sender: MessageTarget, completed: float, speed: float) -> None:
        super().__init__(sender)
        self.completed = completed
        self.speed = speed


empty_span = Span(0, 0, "")


class Screen(Widget):
    def __init__(
        self,
    ):
        super().__init__()

        parser = Parser()
        self.set_paragraph()
        self.min_speed = int(parser.get_data("min_speed"))
        self.min_accuracy = int(parser.get_data("min_accuracy"))
        self.min_burst = int(parser.get_data("min_burst"))
        self.cursor_buddy_speed = int(parser.get_data("cursor_buddy_speed"))
        self.force_correct = parser.get_data("force_correct")
        self.tab_reset = parser.get_data("tab_reset")
        self.difficulty = parser.get_data("difficulty")
        self.restart_same = parser.get_data("restart_same")
        self.blind_mode = parser.get_data("blind_mode")
        self.confidence_mode = parser.get_data("confidence_mode")
        self.single_line_words = parser.get_data("single_line_words")
        self.sound = parser.get_data("sound")
        self.caret_style = parser.get_data("caret_style")

        match self.caret_style:
            case "off":
                self.cursor_style = ""
            case "block":
                self.cursor_style = "reverse"
            case "underline":
                self.cursor_style = "underline"

        self.spaces = [i for i, j in enumerate(self.paragraph.plain) if j == " "] + [
            self.paragraph_length
        ]

        self.started = False
        self.finised = False
        self.failed = False
        self.cursor_position = 0
        self.cursor_buddy_position = 0
        self.correct_key_presses = 0
        self.total_key_presses = 0
        self.mistakes = 0
        self.mistakes_hashmap = dict()
        self.correct = [False] * (self.paragraph_length + 1)

        if self.cursor_buddy_speed:
            self.set_interval(
                60 / (5 * self.cursor_buddy_speed), self.move_cursor_buddy
            )

        self.set_interval(0.2, self._update_race_bar)

    async def _update_race_bar(self):
        if self.started and not self.finised:
            self.raw_speed = (
                60 * self.correct_key_presses / (time.time() - self.start_time) / 5
            )
            self.accuracy = (self.correct_key_presses / self.total_key_presses) * 100
            self.speed = (self.accuracy / 100) * self.raw_speed
            progress = (
                100
                * (self.correct_key_presses + self.mistakes)
                / len(self.paragraph.plain)
            )

            if (
                self.speed < self.min_speed
                or self.accuracy < self.min_accuracy
                or self.failed
            ):
                self.finised = True
                self.failed = True
                self.speed = -1
                self.refresh()

            await self.emit(
                UpdateRaceBar(
                    self,
                    progress,
                    self.speed,
                )
            )
        else:
            await self.emit(UpdateRaceBar(self, 0, 0))

    def _get_color(self, type: str):
        if self.blind_mode == "on":
            return "yellow"
        else:
            return "green" if type == "correct" else "red"

    def move_cursor_buddy(self):
        if self.started:
            if self.cursor_buddy_position < self.paragraph_length - 1:
                self.cursor_buddy_position += 1
                self.refresh()

    async def reset_screen(self):
        self.cursor_position = 0
        self.cursor_buddy_position = 0
        self.correct_key_presses = 0
        self.total_key_presses = 0
        self.started = False
        self.finised = False
        self.failed = False

        if self.restart_same == "on":
            self.paragraph.spans = []
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
        self.paragraph_length = len(self.paragraph.plain)
        self.refresh()

    def report(self):
        if self.failed:
            return "FAILED"
        else:
            return (
                "\n"
                + f"RAW SPEED            : {self.raw_speed:.2f} WPM"
                + "\n"
                + f"CORRECTED SPEED      : {self.speed:.2f} WPM"
                + "\n"
                + f"ACCURACY             : {self.accuracy:.2f} %"
                + "\n"
                + f"TIME TAKEN           : {time.time() - self.start_time:.2f} seconds"
            )

    async def key_add(self, key: str):
        if key == "ctrl+i":  # TAB
            await self.reset_screen()

        if self.sound:
            self.console.bell()

        if key == "ctrl+h":  # BACKSPACE
            if self.confidence_mode == "max":
                return

            if self.cursor_position:
                if (
                    self.confidence_mode == "on"
                    and self.paragraph.plain[self.cursor_position - 1] == " "
                ):
                    return

                if self.correct[self.cursor_position]:
                    self.correct_key_presses -= 1

                self.cursor_position -= 1
                self.paragraph.spans.pop()

        elif len(key) == 1:
            self.total_key_presses += 1
            if key == " ":
                if self.paragraph.plain[self.cursor_position] != " ":
                    if self.force_correct == "off":
                        next_space = self.spaces[
                            bisect(self.spaces, self.cursor_position)
                        ]
                        difference = (
                            next_space - self.cursor_position + 1
                        )  # 1 for the next space
                        self.paragraph.spans.extend([empty_span] * difference)
                        self.cursor_position = next_space
                    else:
                        return
                else:
                    if self.difficulty == "expert" and self.mistakes:
                        self.failed = True

                    self.correct_key_presses += 1
                    self.paragraph.spans.append(empty_span)

            elif key == self.paragraph.plain[self.cursor_position]:
                self.paragraph.spans.append(
                    Span(
                        self.cursor_position,
                        self.cursor_position + 1,
                        self._get_color("correct"),
                    )
                )
                self.correct_key_presses += 1
                self.correct[self.cursor_position] = True

            else:
                if (
                    self.paragraph.plain[self.cursor_position] == " "
                    or self.force_correct == "on"
                ):
                    return

                self.paragraph.spans.append(
                    Span(
                        self.cursor_position,
                        self.cursor_position + 1,
                        self._get_color("mistake"),
                    )
                )

                self.mistakes += 1
                if self.difficulty == "master":
                    self.failed = True

            self.cursor_position += 1
            if not self.started:
                self.start_time = time.time()
            self.started = True

            if self.cursor_position == self.paragraph_length:
                self.finised = True

        self.refresh()

    def render(self):
        if not self.finised and not self.failed:
            return Panel(
                Text(
                    self.paragraph.plain,
                    spans=self.paragraph.spans
                    + [
                        Span(
                            self.cursor_position,
                            self.cursor_position + 1,
                            self.cursor_style,
                        )
                    ]
                    + [
                        Span(
                            self.cursor_buddy_position,
                            self.cursor_buddy_position + 1,
                            "reverse magenta",
                        )
                        if self.cursor_buddy_speed
                        else empty_span
                    ],
                )
            )

        else:
            return Panel(Align.center(Text(self.report()), vertical="middle"))


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.x = Screen()
            await self.view.dock(self.x)

    MyApp.run()
