from termtyper.events.events import BarThemeChange, ParaSizeChange
from termtyper.ui.widgets.menu import Menu


class SizeMenu(Menu):
    def __init__(self):
        options = ["teensy", "small", "big", "huge"]
        super().__init__(
            "size_menu",
            options,
            ParaSizeChange,
            draw_border=True,
            title="How much can your fingers handle?",
        )


class BarThemeMenu(Menu):
    def __init__(self):
        options = ["minimal", "pacman", "doge", "ballon", "rust"]
        super().__init__(
            "bar_theme_menu",
            options,
            BarThemeChange,
            draw_border=True,
            title="Choose your theme",
        )
