from textual.widget import Widget


class Palette(Widget):
    DEFAULT_CSS = """
    Palette {
        margin: 0 3;
        width: auto;
        height: 1;
    }
    """

    screen_name: str

    def on_click(self, event):
        self.app.push_screen(self.screen_name)
