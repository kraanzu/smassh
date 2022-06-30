from termtyper.events.events import BarThemeChange, ParaSizeChange
from termtyper.ui.widgets.menu import Menu


class SizeMenu(Menu):
    def __init__(self):
        options = ["teensy", "small", "big", "huge"]
        super().__init__(
            "paragraph_size",
            options,
            ParaSizeChange,
            draw_border=True,
            title="How much can your fingers handle?",
            section="user",
        )


class BarThemeMenu(Menu):
    def __init__(self):
        options = ["minimal", "pacman", "doge", "ballon", "rust"]
        super().__init__(
            "bar_theme",
            options,
            BarThemeChange,
            draw_border=True,
            title="Choose your theme",
            section="theming",
        )
