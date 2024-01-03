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

    async def on_click(self, _) -> None:
        await self.app.push_screen(self.screen_name)
        self.app.refresh_css(animate=False)
