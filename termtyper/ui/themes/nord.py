from .base import Theme


class NordTheme(Theme):
    WHITE: str = "#ECEFF4"
    BLACK: str = "#2E3440"
    RED: str = "#BF616A"
    GREEN: str = "#A3BE8C"
    YELLOW: str = "#EBCB8B"
    BLUE: str = "#5E81AC"
    MAGENTA: str = "#B48EAD"
    CYAN: str = "#88C0D0"

    SCREEN_BG: str = f"{BLACK} 80%"
    HEADER_BG: str = BLACK
    BRAND: str = CYAN
    NAVITEM_HOVER: str = BLUE
    NAVITEM_ACTIVE: str = f"bold {CYAN}"
    HELP_HEADER: str = f"bold {BLUE}"
    HELP_TEXT: str = YELLOW
    OUTRO_TEXT: str = MAGENTA
    SETTINGS_HEADER: str = f"bold {BLUE}"
    SETTINGS_SECTION: str = GREEN
    SETTINGS_TEXT: str = YELLOW
    SETTINGS_OPTION: str = CYAN
