import time
from itertools import accumulate
from os import get_terminal_size
from textwrap import wrap
from bisect import bisect, bisect_right
from rich.align import Align
from rich.box import MINIMAL
from rich.console import RenderableType
from rich.text import Span, Text, TextType
from rich.panel import Panel
from textual.app import App
from textual.widget import Widget

from ...utils import generate, play_keysound, play_failed
from ...utils.parser import MAIN_PARSER
from ...events import UpdateRaceHUD, ResetHUD

EMPTY_SPAN = Span(0, 0, "")
x, y = get_terminal_size()
HEIGHT = round(0.75 * y)
WIDTH = round(0.80 * x)
parser = MAIN_PARSER


class Screen(Widget):
    def __init__(self, quiet: bool) -> None:
        super().__init__()
        self.quiet = quiet
        self._reset_params()
        self.set_interval(0.2, self._update_race_hud)

    async def _refresh_settings(self) -> None:
        self.min_speed = int(parser.get_data("min_speed"))
        self.min_accuracy = int(parser.get_data("min_accuracy"))
        self.min_burst = int(parser.get_data("min_burst"))
        self.cursor_buddy_speed = int(parser.get_data("cursor_buddy_speed"))
        self.force_correct = parser.get_data("force_correct")
        self.tab_reset = parser.get_data("tab_reset")
        self.difficulty = parser.get_data("difficulty")
        self.blind_mode = parser.get_data("blind_mode")
        self.confidence_mode = parser.get_data("confidence_mode")
        self.single_line_words = parser.get_data("single_line_words")
        self.caret_style = parser.get_theme("caret_style")
        self.allow_numbers = parser.get_para_setting("numbers")
        self.allow_puncs = parser.get_para_setting("punctuations")
        self.allow_cap = parser.get_data("capitalization_mode")
        self.mode = parser.get("mode", "writing mode")
        self.timeout = int(parser.get("user", "timeout"))
        self.keypress_sound = parser.get_theme("keypress_sound")
        self.language = parser.get_data("language")
        self.set_paragraph()

        match self.caret_style:
            case "off":
                self.cursor_style = ""
            case "block":
                self.cursor_style = "reverse"
            case "underline":
                self.cursor_style = "underline"

        if hasattr(self, "buddy_timer"):
            await self.buddy_timer.stop()

        if self.cursor_buddy_speed:
            self.buddy_timer = self.set_interval(
                60 / (5 * self.cursor_buddy_speed), self.move_cursor_buddy
            )

    def _get_color(self, type: str) -> str:
        """
        returns color for typed letter
        """

        if self.blind_mode == "on":
            return "yellow"
        else:
            return "green" if type == "correct" else "red"

    def _reset_params(self) -> None:
        """
        resets everyting on typing start
        """

        self.started = False
        self.finished = False
        self.failed = False
        self.speed = 0
        self.min_speed = 0
        self.cursor_position = 0
        self.cursor_buddy_position = 0
        self.correct_key_presses = 0
        self.total_key_presses = 0
        self.mistakes = 0

    def _get_previous_character(self) -> str:
        # well there were multiple places where this was needed.
        # why not make a function? ;)
        return self.paragraph.plain[self.cursor_position - 1]

    def _update_speed_records(self) -> None:
        """
        Updates speed records when the typing is over
        """

        if self.speed == -1:
            return

        med = (parser.get_speed("med") + self.speed) / 2
        parser.set_speed("med", med)

        low = min(parser.get_speed("low"), self.speed)
        parser.set_speed("low", low)

        high = max(parser.get_speed("high"), self.speed)
        parser.set_speed("high", high)

    def _update_measurements(self) -> None:
        """
        Recalibrate the measurements for speed, accuracy and progress
        """

        correct = self.correct_key_presses
        total = self.total_key_presses
        mistake = self.mistakes

        self.raw_speed = 60 * correct / (time.time() - self.start_time) / 5
        self.accuracy = (correct / total) * 100
        self.speed = (self.accuracy / 100) * self.raw_speed
        self.progress = (correct + mistake) / len(self.paragraph.plain)

        if (
            self.speed < self.min_speed
            or self.accuracy < self.min_accuracy
            or self.failed
        ):
            self.finished = True
            self.finish_time = time.time()
            self.failed = True
            self.speed = -1
            play_failed()

    async def _update_race_hud(self) -> None:
        """
        Simultaneously updates race HUD with typing
        """

        if self.started and not self.finished:

            self._update_measurements()
            if self.mode == "words":
                progress = self.progress
            else:
                progress = time.time() - self.start_time
                progress = (self.timeout - progress) / self.timeout
                if progress < 0:
                    self.end_typing()

            await self.emit(UpdateRaceHUD(self, progress, self.speed, self.accuracy))

            self.refresh()
        else:
            if self.mode == "words":
                await self.emit(UpdateRaceHUD(self, 0, 0, 0))
            else:
                await self.emit(UpdateRaceHUD(self, 1, 0, 0))

    def move_cursor_buddy(self) -> None:
        """
        Manages the cursor buddy if set
        """

        if self.started:
            if self.cursor_buddy_position < self.paragraph_length - 1:
                self.cursor_buddy_position += 1
                self.refresh()

    async def reset_screen(self, restart_same=parser.get_data("restart_same")) -> None:
        """
        Reset the screen when left in mid of typing or re-started
        """

        self._reset_params()
        await self._refresh_settings()
        if restart_same == "on":
            self.paragraph.spans = []
        else:
            self.set_paragraph()

        await self.emit(ResetHUD(self))
        self.refresh()

    def set_paragraph(self) -> None:
        """
        Sets the paragraph for the Screen
        """

        if self.mode == "words":
            size = parser.get_data("paragraph_size")
            if size == "teensy":
                times = 1
            elif size == "small":
                times = 5
            elif size == "big":
                times = 10
            else:
                times = 15
        else:
            times = 100

        paragraph = (
            generate(
                times,
                (self.allow_numbers),
                (self.allow_puncs),
                self.allow_cap,
                self.language,
            )
            + " "
        )
        self.paragraph = Text(paragraph)
        self.wrapped = [0] + list(
            accumulate([len(i) + (len(i) != WIDTH) for i in wrap(paragraph, WIDTH)])
        )
        self.paragraph_length = len(self.paragraph.plain)

        self.spaces = [i for i, j in enumerate(paragraph) if j == " "]
        self.correct = [False] * (self.paragraph_length + 1)
        self.refresh()

    def report(self) -> TextType:
        """
        Generates a report when the typing is finised
        """

        highest_score = parser.get_speed("high")
        style = "bold red"
        if self.failed:
            return f"[{style}]FAILED[/{style}]"
        else:
            return (
                "\n"
                + f"[{style}]RAW SPEED[/{style}]            : {self.raw_speed:.2f} WPM"
                + "\n"
                + f"[{style}]CORRECTED SPEED[/{style}]      : {self.speed:.2f} WPM"
                + "\n"
                + f"[{style}]ACCURACY[/{style}]             : {self.accuracy:.2f} %"
                + "\n"
                + f"[{style}]TIME TAKEN[/{style}]           : {self.finish_time - self.start_time:.2f} seconds"
                + "\n"
                + f"[{style}]HIGHEST SCORE[/{style}]        : {highest_score:.2f} WPM"
            )

    def _is_key_correct(self) -> bool:
        """Check if the current pressed key matches with the current cursor position"""

        return self.pressed_key == self.paragraph.plain[self.cursor_position]

    def _check_min_burst(self) -> bool:
        """
        Check if the min_burst rule is violated
        """

        pos = self.cursor_position - 1
        correct = 0
        total = 0
        while pos >= 0 and self.paragraph.plain[pos] != " ":
            correct += self.correct[pos]
            total += 1
            pos -= 1

        return (100 * correct / total) >= self.min_burst

    async def key_add(self, key: str) -> None:
        """
        Process the pressed key
        """

        if key == "ctrl+i" and self.tab_reset == "on":  # TAB
            await self.reset_screen()

        if self.finished:
            return

        if (
            not self.quiet
            and self.keypress_sound != "off"
            and not (key == "ctrl+h" and self.keypress_sound != "backspace")
        ):
            play_keysound()

        self.pressed_key = key

        if key == "ctrl+w":
            if self.cursor_position and self._get_previous_character() == " ":
                await self.key_add("ctrl+h")

            while self.cursor_position and self._get_previous_character() != " ":
                await self.key_add("ctrl+h")

        elif key == "ctrl+h":  # BACKSPACE
            if self.confidence_mode == "max":
                return

            if self.cursor_position:
                if (
                    self.confidence_mode == "on"
                    and self._get_previous_character() == " "
                ):
                    return

                if self.correct[self.cursor_position]:
                    self.correct_key_presses -= 1
                else:
                    self.mistakes -= 1

                self.cursor_position -= 1
                self.paragraph.spans.pop()

        elif len(key) == 1:
            self.total_key_presses += 1
            if key == " ":
                if not self._is_key_correct():
                    if (
                        self.force_correct == "off"
                        and self.cursor_position
                        and self._get_previous_character() != " "
                    ):
                        next_space = self.spaces[
                            bisect(self.spaces, self.cursor_position)
                        ]
                        difference = (
                            next_space - self.cursor_position + 1
                        )  # 1 for the next space
                        self.paragraph.spans.extend([EMPTY_SPAN] * difference)
                        self.mistakes += difference
                        self.cursor_position = next_space
                        if not self._check_min_burst():
                            self.failed = True
                    else:
                        return
                else:

                    if self.difficulty == "expert" and self.mistakes:
                        self.failed = True
                    if not self._check_min_burst():
                        self.failed = True

                    self.correct_key_presses += 1
                    self.paragraph.spans.append(EMPTY_SPAN)

            elif self._is_key_correct():
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

            if self.cursor_position > self.paragraph_length - 1:
                await self._update_race_hud()
                self.end_typing()

        self.refresh()

    def end_typing(self):
        self.finished = True
        self.finish_time = time.time()
        self.refresh()

    def find_cursor(self) -> int:
        pos = bisect_right(self.wrapped, self.cursor_position)
        return max(1, min(len(self.wrapped) - 2, pos) - 1)

    def render(self) -> RenderableType:
        line = self.find_cursor()
        if not self.finished and not self.failed:
            return Align.center(
                Panel(
                    Text(
                        self.paragraph.plain,
                        spans=self.paragraph.spans
                        + [
                            Span(
                                self.cursor_position + 1,
                                len(self.paragraph.plain),
                                "dim white",
                            )
                        ]
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
                            else EMPTY_SPAN
                        ],
                    )[
                        self.wrapped[line - 1] : self.wrapped[
                            min(len(self.wrapped) - 1, line + 2)
                        ]
                    ],
                    width=WIDTH + 4,
                    box=MINIMAL,
                ),
                vertical="middle",
                height=HEIGHT,
            )

        else:
            self._update_speed_records()
            return Panel(
                Align.center(self.report(), vertical="middle", height=HEIGHT),
                box=MINIMAL,
            )


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.x = Screen()
            await self.view.dock(self.x)

    MyApp.run()
