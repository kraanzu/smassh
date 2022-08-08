from os import get_terminal_size
from typing import Literal
from rich.text import Text
from textual.widget import Widget

BarStyle = Literal["minimal", "pacman", "rust", "doge", "balloon"]
Segment = tuple[str, str]


def ceil(a, b):
    return (a + b) // b


class ProgressBar(Widget):
    def __init__(
        self,
        total: float,
        completed: float,
        bar_style: BarStyle = "minimal",
        color: str = "white",
    ) -> None:
        self.total = total
        self.completed = completed
        self.bar_style = bar_style
        self.color = color
        self.width = round(0.8 * get_terminal_size()[0])

    def style_text(self, segment: Segment) -> Text:
        return Text.from_markup(segment[0], style=self.color,) + Text.from_markup(
            segment[1],
            style="d black",
        )

    def render_balloon(self, done, rem):
        total = done + rem
        bg = "⠁⠈⠐⠠⢀⡀⠄⠂"
        bg = bg * ceil(total, len(bg))
        return bg[: max(done - 1, 0)] + "🎈", bg[done : done + rem]

    def render_minimal(self, done, rem) -> Segment:
        pre = "━" * done
        suf = "━" * rem
        return pre, suf

    def render_doge(self, done, rem):
        pre = "$" * (done - 2) + " "
        pre += "[yellow]:dog:[/yellow]"
        suf = "━" * rem
        suf += "🌝"
        return pre, suf

    def render_rust(self, done, rem) -> Segment:
        pre = "━" * (done - 1)
        pre += ":crab:"
        suf = "━" * rem
        self.color = "orange1"
        return pre, suf

    def render_pacman(self, done, rem) -> Segment:
        pre = ("-" * (done - 1)) + ("c" if done % 2 else "C")
        suf = ("● " if done % 2 else " ●") * rem
        suf = suf[:rem]
        return pre, suf

    def render(self) -> Text:
        done = round(self.completed / self.total * self.width)
        rem = self.width - done
        segment = eval(f"self.render_{self.bar_style}({done}, {rem})")
        return self.style_text(segment)
