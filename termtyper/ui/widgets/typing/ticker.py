from textual.widget import Widget


class Ticker(Widget):
    def __init__(self, text: str = "", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = text

    def update(self, value: str) -> None:
        self.text = value
        self.refresh()

    def render(self) -> str:
        return self.text
