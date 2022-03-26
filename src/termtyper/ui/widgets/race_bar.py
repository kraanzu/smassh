from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.widget import Widget
from rich.progress_bar import ProgressBar
from ...utils import Parser


class RaceBar(Widget):
    """
    A progress bar widget that shows the progress of writing
    with colors accoring to the speed of the typer
    """

    def __init__(
        self,
        name: str | None = None,
        total: float = 1,
    ) -> None:
        super().__init__(name)
        self.completed = 0
        self.total = total
        self.speed = 0
        self.finised = False
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
        self.finised = False
        self.completed = False

    def update(self, progress: float, speed: float):
        """
        Updates the bar with the most current measurements
        """

        if not self.finised:
            self.completed = progress
            self.finised = progress == 1 or speed == -1
            self.speed = speed
            self.remarks = self.get_remarks()
            self.refresh()

    def render(self) -> RenderableType:
        return Panel(
            Align.center(
                ProgressBar(
                    total=self.total,
                    completed=self.completed,
                    complete_style="bold " + self.get_speed_color(),
                )
                if not self.finised
                else Text(self.remarks, style="bold green"),
                vertical="middle",
            )
        )


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.plus = 5
            self.x = RaceBar()
            self.set_interval(0.1, self.inc)
            await self.view.dock(self.x, size=5)

        def inc(self):
            self.plus += 5
            self.x.update(self.plus, 500)

    MyApp.run()
