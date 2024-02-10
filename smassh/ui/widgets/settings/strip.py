from textual.widget import Widget
from textual.widgets import Label


class SettingStripItem(Label):
    DEFAULT_CSS = """
    SettingStripItem {
        color: white;
        padding: 0 2;
        height: 1;
    }
    """


class SettingStrip(Widget):
    DEFAULT_CSS = """
    SettingStrip {
        height: 1;
        layout: horizontal;
        width: 100%;
        align: center middle;
    }
    """
