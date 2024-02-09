import os
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static

from smassh.ui.widgets.label import Banner, NavItem


def get_username() -> str:
    try:
        username = os.getlogin()
    except OSError:
        uid = os.getuid()
        import pwd

        username = pwd.getpwuid(uid).pw_name

    return username


class Header(Widget):
    """
    Header which forms the top banner of the app
    """

    DEFAULT_CSS = """
    Header {
        layout: grid;
        grid-size: 4 1;
        grid-rows: 5;
        grid-columns: 1fr 15 8fr 1fr;
    }

    Header > Horizontal {
        align: left middle;
        height: 100%;
    }
    """

    def on_resize(self) -> None:
        # XXX: Why use screen size and not widget size?
        # Ans: Because this can change the widget size (be it header or container)
        #      which will trigger this method again, causing an infinite loop
        height = self.screen.size.height

        # NOTE: This seems like a good ratio (5:30) to enable/disable tall mode
        if height < 30:
            self.disable_tall_mode()
        else:
            self.enable_tall_mode()

        self.refresh(layout=True)

    def enable_tall_mode(self) -> None:
        height = self.size.height
        if height == 5:
            return

        self.screen.styles.grid_rows = "5 1fr"
        self.query_one(Banner).is_tall = True
        self.query_one("Header > Horizontal").styles.height = "5"

    def disable_tall_mode(self) -> None:
        height = self.size.height
        if height != 5:
            return

        self.screen.styles.grid_rows = "3 1fr"
        self.query_one(Banner).is_tall = False
        self.query_one("Header > Horizontal").styles.height = "3"

    def set_active(self, name: str) -> None:
        for i in self.query(NavItem):
            i.set_class(i.screen_name == name, "active")

    def compose(self) -> ComposeResult:
        yield Static()
        yield Banner("smassh")

        with Horizontal():
            home = NavItem("󰌌 home", "typing")
            home.add_class("active")

            yield home
            yield NavItem(" settings", "settings")
            yield NavItem("󰋗 help", "help")
            yield NavItem(" about", "about")

        # yield NavItem("  " + get_username())
