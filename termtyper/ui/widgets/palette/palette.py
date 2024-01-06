from rich.console import RenderableType
from termtyper.src.parser import config_parser
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
    config_name: str
    icon: str

    @property
    def current(self) -> str:
        return config_parser.get(self.config_name)

    async def on_click(self, _) -> None:
        await self.app.push_screen(self.screen_name)
        self.app.refresh_css(animate=False)

    def render(self) -> RenderableType:
        return f"{self.icon} {self.current}"
