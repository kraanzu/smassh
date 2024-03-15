from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget


class SettingSeparator(Widget):
    DEFAULT_CSS = """
    SettingSeparator {
        height: auto;
        width: 100%;
        text-style: bold italic;
        margin: 1 0;
    }
    """

    COMPONENT_CLASSES = {"--primary-bg", "--danger-bg"}

    def __init__(self, section: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.section = section

    def render(self) -> RenderableType:
        classname = "danger" if "danger" in self.section else "primary"
        style = self.get_component_rich_style(f"--{classname}-bg")

        text = Text(self.section.upper().replace("_", " "), style=style)
        text.pad(1)
        return text
