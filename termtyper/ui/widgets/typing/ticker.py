from textual.widget import Widget
from termtyper.src import config_parser


class Ticker(Widget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reset()
        self.set_interval(1, self.update)

    def update(self) -> None:
        from termtyper.ui.widgets import Space

        mode = config_parser.get("mode")
        stats = self.screen.query_one(Space).tracker.stats
        if mode == "words":
            self.text = str(stats.word_count)
        else:
            if stats.start_time:
                count = config_parser.get("time_count")
                time_remaining = count - stats.elapsed_time
                self.text = str(round(time_remaining))

        self.refresh()

    def reset(self):
        mode = config_parser.get("mode")
        if mode == "words":
            self.text = "0"
        else:
            count = config_parser.get("time_count")
            self.text = str(count)

        self.refresh()

    def render(self) -> str:
        return self.text
