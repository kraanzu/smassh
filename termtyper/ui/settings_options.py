from typing import Union
from collections import OrderedDict
from rich import box
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from textual.events import Key
from textual.widget import Widget
from termtyper.events.events import LoadScreen

from ..utils.getting_started import colored
from ..ui.widgets import Option, NumberScroll, banners

SettingWidget = Union[Option, NumberScroll]


class Setting:
    """
    A class that holds one setting for the termtyper!
    """

    def __init__(
        self, title: str, items: dict[str, str], widget: SettingWidget, info: str = ""
    ) -> None:
        self.title = title
        self.items = items
        self.widget = widget
        self.info = info
        if self.info:
            self.info += "\n"

        self.description = self.render_description()

    def select(self):
        self.widget.highlight()

    def deselect(self):
        self.widget.lowlight()

    def select_next(self):
        self.widget.select_next_option()

    def select_prev(self):
        self.widget.select_prev_option()

    def render_description(self) -> str:
        c1 = "bold blue"
        c2 = "yellow"
        c3 = "cyan"
        return (
            f"[{c1}]{self.title}[/{c1}]"
            + "\n"
            + f"[{c2}]{self.info}[/{c2}]"
            + "\n".join(
                f"[{c3}]{sub}[/{c3}]: {desc}" for sub, desc in self.items.items()
            )
        )


class SettingMenu(Widget):
    """
    A menu class for showing multiple settings in one page
    """

    def __init__(self, ascii_art: RenderableType, items: list[Setting]):
        self.ascii_art = ascii_art
        self.items = items
        self.height = max(i.description.count("\n") for i in items) + 1
        self._total = len(items)
        self.selected_index = 0
        self.update()

    def select_next_setting(self):
        self.selected_index = (self.selected_index + 1) % self._total
        self.update()

    def select_prev_setting(self):
        self.selected_index = (self.selected_index - 1 + self._total) % self._total
        self.update()

    def select_next_setting_option(self):
        self.items[self.selected_index].select_next()

    def select_prev_setting_option(self):
        self.items[self.selected_index].select_prev()

    def update(self):
        for index, setting in enumerate(self.items):
            if index == self.selected_index:
                setting.select()
            else:
                setting.deselect()

    def render(self) -> RenderableType:
        table = Table.grid(expand=True)
        table.add_column("Desc", ratio=80)
        table.add_column("Opts", ratio=20)

        for index, i in enumerate(self.items):
            table.add_row(
                Panel(
                    i.render_description(),
                    height=8,
                    border_style="magenta" if index == self.selected_index else "",
                    box=box.HEAVY,
                ),
                i.widget,
            )

        return table


menu: dict[str, SettingMenu] = OrderedDict()

# First menu
menu["push_your_limits"] = SettingMenu(
    banners["push_your_limits"],
    [
        Setting(
            "Min Speed",
            {},
            NumberScroll("min_speed", section="user"),
            info="Are you fast enough?"
            + "\n"
            + "Note: If your speed falls below this speed you will be declared failed",
        ),
        Setting(
            "Min Accuracy",
            {},
            NumberScroll("min_accuracy", section="user"),
            info="You can't go wrong with this"
            + "\n"
            + "Note: If your accuracy falls below this accuracy you will be declared failed",
        ),
        Setting(
            "Min Burst:",
            {},
            NumberScroll("min_burst", section="user"),
            info="Wanna make your life harder?"
            + "\n"
            + "Note: If your accuracy for a word falls below this accuracy you will be declared failed",
        ),
    ],
)

# Second Menu
menu["hardcore"] = SettingMenu(
    banners["hardcore"],
    [
        Setting(
            "Difficulty",
            {
                "normal": "You can type at your own accuracy",
                "expert": "Moving forward without writing the prev word correctly? YOU'RE FAILED!",
                "master": "A single incorrect press will declare you failed",
            },
            Option(
                name="difficulty",
                options=["normal", "expert", "master"],
                section="user",
            ),
            "Where's the fun without some conditions?",
        ),
        Setting(
            "Blind Mode",
            {
                "off": "You will get to know whether you typed right or  wrong",
                "on": "Just believe your spidey sense!",
            },
            Option(name="blind_mode", options=["off", "on"], section="user"),
            "Have a lot of Confidence? Try this !"
            + "\n"
            + "Note: You should turn [bold]force correct[/bold] off if you are turing blind mode on",
        ),
    ],
)


# Third Menu

menu["discipline"] = SettingMenu(
    banners["discipline"],
    [
        Setting(
            "Force correct",
            {
                "on": "You will not be allowed to move forward until"
                + "\n"
                + "and unless all the characters until your cursor are typed correctly",
                "off": "You live your life your own way!",
            },
            Option(name="force_correct", options=["off", "on"], section="user"),
            "Are you worthy?",
        ),
        Setting(
            "Confidence Mode:",
            {
                "off": "You can type backspace as many times you want",
                "on": "You will only be able to backspace until the start of the current word",
                "max": "You will not be able to press backspace at all",
            },
            Option(
                name="confidence_mode", options=["off", "on", "max"], section="user"
            ),
            "Feeling Lucky?",
        ),
        Setting(
            "Capitalization Mode:",
            {
                "off": "All lowercase words, don't worry about your 'Shift' key",
                "on": "You will come across some words that start with a capital letter, but not many",
                "max": "Try a mixed-case word trial",
            },
            Option(
                name="capitalization_mode", options=["off", "on", "max"], section="user"
            ),
            "Getting your hands dirty?",
        ),
    ],
)

# Fourth Menu
menu["eye_candy"] = SettingMenu(
    banners["eye_candy"],
    [
        Setting(
            "Caret style",
            {
                "off": "[green]hello pete[/green]r",
                "underline": "[green]hello pete[/green][underline]r[/underline]",
                "block": "[green]hello pete[/green][reverse]r[/reverse]",
            },
            Option(
                name="caret_style",
                options=["off", "underline", "block"],
                section="theming",
            ),
            info="Choose your style!",
        ),
        Setting(
            "Cursor buddy",
            {},
            NumberScroll("cursor_buddy_speed", section="user"),
            info="Feeling a little lonely?"
            + "\n"
            + "A cursor will race along with you with this constant speed."
            + "\n"
            + "'0' means it will not be visible",
        ),
    ],
)

# Fifth Menu
menu["aesthetics"] = SettingMenu(
    banners["aesthetics"],
    [
        Setting(
            "Keypress Sound",
            {
                "off": "Already have good switches? There will be no sound on keypress",
                "on": "Pressing a key will trigger a click sound except backspace",
                "backspace": "Pressing key, including backspace, will trigger click sound",
            },
            Option(
                name="keypress_sound",
                options=["off", "on", "backspace"],
                section="theming",
            ),
            "Sounds good?",
        ),
        Setting(
            "Click sound",
            {
                "cream": "Smooth soothing sound to the ears :)",
                "lubed": "Just the right amount",
                "mech": "Mechanical feel baby!",
                "heavy": "Wanna feel like you are on a typewriter?",
            },
            Option(
                "sound",
                options=["cream", "lubed", "mech", "heavy"],
                section="theming"
                # callback=play_keysound,
            ),
            "Choose whats most pleasing to you ears :)",
        ),
    ],
)

# Sixth Menu
menu["misc"] = SettingMenu(
    banners["misc"],
    [
        Setting(
            "Tab Reset",
            {
                "on": "Pressing tab will cancel the current typing and re-start it",
                "off": "Pressing tab will have no effect ",
            },
            Option(name="tab_reset", options=["off", "on"], section="user"),
            "Lost your gusto in the middle of typing? Restart by hitting a tab!",
        ),
        Setting(
            "Restart Same",
            {
                "off": "Pressing tab will render a new paragraph",
                "on": "Pressing tab will restart the typing session with the same paragraph",
            },
            Option(name="restart_same", options=["off", "on"], section="user"),
            "Wanna practice the same paragraph over and over? This option is for you!",
        ),
        Setting(
            "Language",
            {},
            Option(
                name="language", 
                options=["english", "french"], 
                section="user"
            ),
            "Choose the language you want the words to be generated from !",
        )
    ],
)


class MenuSlide(Widget):
    def __init__(self, menus=list(menu.values())):
        super().__init__()
        self.menus = menus
        self._current = 0

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, val: int):
        _total = len(self.menus)
        self._current = (val + _total) % _total
        self.refresh()

    @property
    def curr_menu(self):
        return self.menus[self.current]

    def next(self):
        self.current += 1

    def prev(self):
        self.current -= 1

    def banner(self) -> Panel:
        banner = self.menus[self.current].ascii_art
        banner.title = f"Press {colored('ctrl+h','b green')} for help"
        banner.title_align = "right"
        return banner

    async def key_press(self, event: Key):
        match event.key:
            case "j" | "down":
                self.curr_menu.select_next_setting()
            case "k" | "up":
                self.curr_menu.select_prev_setting()
            case "J" | "shift+down":
                self.curr_menu.select_next_setting_option()
            case "K" | "shift+up":
                self.curr_menu.select_prev_setting_option()
            case "ctrl+i":
                self.next()
            case "shift+tab":
                self.prev()
            case "escape":
                await self.post_message(LoadScreen(self, "main_menu"))

        self.refresh()

    def render(self) -> RenderableType:
        return self.menus[self.current].render()
