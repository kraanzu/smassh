from textual.widget import Widget
from smassh.src import settings


class Ticker(Widget):
    """
    Ticker widget to show time/word left
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.update_check = self.set_interval(0.1, self.update)
        self.reset()

    def update(self) -> None:
        from smassh.ui.widgets import Space

        mode = settings.get("mode")
        stats = self.screen.query_one(Space).tracker.stats

        if not stats.start_time:
            return

        if mode == "words":
            count = settings.get("words_count")
            words_typed = stats.word_count
            self.text = f"{words_typed}/{count}"
        else:
            if stats.start_time:
                count = settings.get("time_count")
                time_remaining = count - stats.elapsed_time
                if time_remaining <= 0:
                    return self.screen.query_one(Space).finish_typing(fail=False)

                self.text = str(round(time_remaining))

        self.refresh()

    def reset(self) -> None:
        self.update_check.pause()
        mode = settings.get("mode")
        if mode == "words":
            count = settings.get("words_count")
            self.text = f"0/{count}"
        else:
            count = settings.get("time_count")
            self.text = str(count)

        self.refresh()

    def render(self) -> str:
        return self.text
