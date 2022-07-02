from rich.align import Align
from rich.box import MINIMAL
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.widget import Widget

from termtyper.ui.widgets.progress_bar import ProgressBar
from ...utils import Parser


class RaceHUD(Widget):
    """
    A dashboard widget that shows the progress of writing
    with colors accoring to the speed of the typer
    """

    def __init__(
        self,
        name: str | None = None,
        total: float = 1,
    ) -> None:
        super().__init__(name)
        self.completed = 0
        self.accuracy = 0
        self.total = total
        self.speed = 0
        self.finished = False
        self.details = False
        self.theme = Parser().get_theme("bar_theme")
        self.mode = Parser().get("mode", "writing mode")
        self._read_speed_records()

    def toggle_details(self):
        self.details = not self.details

    def _read_speed_records(self) -> None:
        self.low = Parser().get_speed("low")
        self.med = Parser().get_speed("med")
        self.high = Parser().get_speed("high")

    def get_speed_color(self) -> str:
        """
        returns speed color according to the current speed
        """
        if self.speed < self.low:
            return "white"
        elif self.speed < self.med:
            return "yellow"
        elif self.speed < self.high:
            return "green"
        else:
            return "red"

    def get_remarks(self) -> str:
        """
        Shows a little paraphrase when you either
        complete the typing essay or when failed
        """
        if self.low == 100000:
            return (
                "This is the start of your journey!"
                + "\n"
                + "I expect great things from you!"
            )

        if self.speed <= self.low:
            return "Lame!"
        elif self.speed <= self.med:
            return "When are you going to take this seriously ?"
        elif self.speed < self.high:
            return "You are still at your medium speed!"
        elif self.speed == self.high:
            return "Ah so close! Got to push a bit more"
        else:
            return "Ah yes! `Pushing past your limits` I see"

    def reset(self) -> None:
        """
        reset the bar when the user wants to re-start
        """

        self._read_speed_records()
        self.finished = False
        self.completed = False

    def update(self, progress: float, speed: float, accuracy: float) -> None:
        """
        Updates the HUD with the most current measurements
        """

        if not self.finished:
            self.completed = progress
            self.finished = (
                (progress >= 2 or speed == -1)
                if self.mode == "words"
                else progress <= 0
            )
            self.speed = speed
            self.accuracy = accuracy
            self.remarks = self.get_remarks()
            self.refresh()

    def refresh(self, repaint: bool = True, layout: bool = False) -> None:
        self.theme = Parser().get_theme("bar_theme")
        return super().refresh(repaint, layout)

    def render(self) -> RenderableType:
        return Panel(
            Group(
                *[
                    Align.center(
                        ProgressBar(
                            total=self.total,
                            completed=self.completed,
                            color="bold " + self.get_speed_color(),
                            bar_style=Parser().get_theme("bar_theme"),
                        ).render()
                    ),
                    Align.center(
                        Text(
                            "\n\n\n"
                            + "WPM: {}    Accuracy: {}%    Progress: {}".format(
                                "{:2.2f}".format(self.speed),
                                "{:.2f}".format(self.accuracy),
                                "{:.2%}".format(self.completed),
                            ),
                            style="bold " + self.get_speed_color(),
                        ),
                    )
                    if self.details
                    else "",
                ],
            )
            if not self.finished
            else Align.center(
                Text(self.remarks, style="bold green", justify="center"),
                vertical="middle",
            ),
            box=MINIMAL,
        )


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.plus = 5
            self.x = RaceHUD()
            self.set_interval(0.1, self.inc)
            await self.view.dock(self.x, size=5)

        def inc(self):
            self.plus += 5
            self.x.update(self.plus, 500, 0)

    MyApp.run()
