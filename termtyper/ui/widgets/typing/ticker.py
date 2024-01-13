from textual.widget import Widget
from termtyper.src import config_parser
from termtyper.ui.events import ShowResults


class Ticker(Widget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.update_check = self.set_interval(1, self.update)
        self.reset()

    def update(self) -> None:
        from termtyper.ui.widgets import Space

        mode = config_parser.get("mode")
        stats = self.screen.query_one(Space).tracker.stats

        if mode == "words":
            count = config_parser.get("words_count")
            words_typed = stats.word_count
            finished = words_typed >= count
            self.text = f"{words_typed}/{count}"
        else:
            finished = False
            if stats.start_time:
                count = config_parser.get("time_count")
                time_remaining = count - stats.elapsed_time
                finished = time_remaining <= 0
                self.text = str(round(time_remaining))

        if finished:
            self.update_check.pause()
            self.screen.post_message(ShowResults(stats))

        self.refresh()

    def reset(self):
        mode = config_parser.get("mode")
        if mode == "words":
            count = config_parser.get("words_count")
            self.text = f"0/{count}"
        else:
            count = config_parser.get("time_count")
            self.text = str(count)

        self.update_check.reset()
        self.refresh()

    def render(self) -> str:
        return self.text
