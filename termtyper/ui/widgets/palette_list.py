from textual.app import ComposeResult
from textual.widgets import Label, ListView, ListItem


class PaletteList(ListView):
    def get_options(self):
        return ["english", "french"]

    def compose(self) -> ComposeResult:
        for option in self.get_options():
            yield ListItem(Label(option))
