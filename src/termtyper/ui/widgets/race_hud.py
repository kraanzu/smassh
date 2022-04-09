from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.widget import Widget
from rich.progress_bar import ProgressBar
from ...utils import Parser

from rich.columns import Columns


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
        self._read_speed_records()

    def _read_speed_records(self) -> None:
        self.low = float(Parser().get_speed("low"))
        self.med = float(Parser().get_speed("med"))
        self.high = float(Parser().get_speed("high"))

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

    def reset(self):
        """
        reset the bar when the user wants to re-start
        """

        self._read_speed_records()
        self.finished = False
        self.completed = False

    def update(self, progress: float, speed: float, accuracy: float):
        """
        Updates the HUD with the most current measurements
        """
        if not self.finished:
            self.completed = progress
            self.finished = progress >= 1 or speed == -1
            self.speed = speed
            self.accuracy = accuracy
            self.remarks = self.get_remarks()
            self.refresh()

    def render(self) -> RenderableType:
        return Panel(
            Columns(
                [
                    Panel(
                        Align.center(
                            ProgressBar(
                                total=self.total,
                                completed=self.completed,
                                complete_style="bold " + self.get_speed_color(),
                            )
                        )
                    ),
                    Panel(
                        Text(
                            "WPM: {}    Accuracy: {}%    Progress: {}%".format(
                                "{:.2f}".format(self.speed),
                                "{:.2f}".format(self.accuracy),
                                "{:.2f}".format(self.completed * 100),
                            ),
                            style="bold " + self.get_speed_color(),
                            justify="center",
                        )
                    ),
                ],
            )
            if not self.finished
            else Align.center(
                Text(self.remarks, style="bold green", justify="center"),
                vertical="middle",
            )
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
            self.x.update(self.plus, 500)

    MyApp.run()
