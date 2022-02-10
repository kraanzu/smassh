from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.widget import Widget
from rich.progress_bar import ProgressBar


class RaceBar(Widget):
    """
    A progress bar widget that shows the amount of writing of the typer
    with colors accoring to the speed of the typer
    """

    def __init__(
        self,
        name: str | None = None,
        total: int = 100,
        low: int = 20,
        med: int = 30,
        high: int = 40,
    ) -> None:
        super().__init__(name)
        self.completed = 0
        self.total = total
        self.speed = 0
        self.low = low
        self.med = med
        self.high = high
        self.speed_sum = 0
        self.finised = False

    def get_speed_color(self) -> str:
        if self.speed < self.low:
            return "white"
        elif self.speed < self.med:
            return "yellow"
        elif self.speed < self.high:
            return "green"
        else:
            return "red"

    def get_remarks(self):
        if self.low == 0:
            return (
                "This is the start of your journey!"
                + "\n"
                + "I expect great things from you!"
            )

        if self.speed <= self.low:
            return "Lame!"
        elif self.speed <= self.med:
            return "You are still at your medium speed!"
        elif self.speed < self.high:
            return "When are you going to take this seriously ?"
        elif self.speed == self.high:
            return "Ah so close! Got to push a bit more"
        else:
            return (
                "Now this is what they say `Pushing past your limits`"
                + "\n"
                + "Keep practicing and go on to become the world's greatest typer"
            )

    def reset(self):
        self.finised = False

    def update(self, progress: float, speed: float):
        if not self.finised:
            self.completed = progress
            self.finised = progress == 100 or speed == -1
            self.speed = speed
            self.remarks = self.get_remarks()
            self.refresh()

    def render(self):
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
