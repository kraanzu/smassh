from textual.screen import Screen


class BaseScreen(Screen):
    DEFAULT_CSS = """
    BaseScreen {
        layout: grid;
        grid-size: 1 2;
        grid-rows: 5 1fr;
    }
    """
