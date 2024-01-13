from textual.widget import Widget
from termtyper.src import config_parser


class Ticker(Widget):
    def __init__(self, text: str = "", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = text

    def update(self, value: str) -> None:
        self.text = value
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
