from textual.widget import Widget


class BaseScroll(Widget):
    DEFAULT_CSS = """
    BaseScroll {
        layout: vertical;
        overflow-y: scroll;
        height: 1fr;
        background: #2e3440;
    }
    """
