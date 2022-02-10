from rich.text import TextType, Text
from textual.widget import Widget
from ui.widgets import Option, NumberScroll
from collections import OrderedDict

c1 = "bold blue"
c2 = "cyan"


class Setting:
    """
    A class that holds one setting for the termtyper!
    """
    def __init__(
        self, title: str, items: dict[str, str], widget: Widget, info: str = ""
    ) -> None:
        self.title = title
        self.items = items
        self.widget = widget
        self.info = info
        if self.info:
            self.info += "\n"

        self.description = self.render_description()

    def render_description(self) -> str:
        return (
            f"[{c1}]{self.title}[/{c1}]"
            + "\n"
            + self.info
            + "\n".join(
                f"[{c2}]{sub}[/{c2}]: {desc}" for sub, desc in self.items.items()
            )
        )


class Menu:
    """
    A menu clas for showing multiple settings in one page
    """
    def __init__(self, ascii_art: str, items: list[Setting]):
        self.ascii_art = ascii_art
        self.items = items
        self.height = max(i.description.count("\n") for i in items) + 1


menu: dict[str, Menu] = OrderedDict()

# First Menu
art_hardcore = """
╦ ╦┌─┐┬─┐┌┬┐┌─┐┌─┐┬─┐┌─┐
╠═╣├─┤├┬┘ │││  │ │├┬┘├┤
╩ ╩┴ ┴┴└──┴┘└─┘└─┘┴└─└─┘
"""
menu["hardcore"] = Menu(
    art_hardcore,
    [
        Setting(
            "Difficulty",
            {
                "normal": "There are no restrictions... you can type at your own accuracy",
                "expert": "Moving to next word without having typed the previous word correctly will declare you failed",
                "master": "You will have to be at 100% accuracy i.e. ...typing even a letter incorrectly will declare your failed",
            },
            Option(name="difficulty", options=["normal", "expert", "master"]),
        ),
        Setting(
            "Blind Mode",
            {
                "off": "You will see green color on the letter if you typed it correctly else red",
                "on": "You will only see yellow color if you have typed that letter",
            },
            Option(name="blind_mode", options=["off", "on"]),
            "You should turn `force correct` off if you are turing blind mode on"
        ),
    ],
)


# Second menu
art_push_your_limits = """
╔═╗┬ ┬┌─┐┬ ┬  ╦ ╦┌─┐┬ ┬┬─┐  ╦  ┬┌┬┐┬┌┬┐┌─┐
╠═╝│ │└─┐├─┤  ╚╦╝│ ││ │├┬┘  ║  │││││ │ └─┐
╩  └─┘└─┘┴ ┴   ╩ └─┘└─┘┴└─  ╩═╝┴┴ ┴┴ ┴ └─┘
"""
menu["push_your_limits"] = Menu(
    art_push_your_limits,
    [
        Setting(
            "Min Speed",
            {},
            NumberScroll("min_speed"),
            info="If your speed falls below this speed you will be declared failed",
        ),
        Setting(
            "Min Accuracy",
            {},
            NumberScroll("min_accuracy"),
            info="If your accuracy falls below this accuracy you will be declared failed",
        ),
        Setting(
            "Min Burst:",
            {},
            NumberScroll("min_burst"),
            info="If your accuracy for a word falls below this accuracy you will be declared failed",
        ),
    ],
)

# Third Menu
art_discipline = """
╔╦╗┬┌─┐┌─┐┬┌─┐┬  ┬┌┐┌┌─┐
 ║║│└─┐│  │├─┘│  ││││├┤
═╩╝┴└─┘└─┘┴┴  ┴─┘┴┘└┘└─┘
"""
menu["discipline"] = Menu(
    art_discipline,
    [
        Setting(
            "Force correct",
            {},
            Option(name="force_correct", options=["off", "on"]),
            info="You will not be allowed to move forward until and unless all the characters uptil your cursor are typed correctly",
        ),
        Setting(
            "Confidence Mode:",
            {
                "off": "You can type backspace as many times you want",
                "on": "You will only be able to backspace until the start of the current word",
                "max": "You will not be able to press backspace at all",
            },
            Option(name="confidence_mode", options=["off", "on", "max"]),
        ),
    ],
)

# Fourth Menu
art_eye_candy = """
╔═╗┬ ┬┌─┐  ╔═╗┌─┐┌┐┌┌┬┐┬ ┬
║╣ └┬┘├┤   ║  ├─┤│││ ││└┬┘
╚═╝ ┴ └─┘  ╚═╝┴ ┴┘└┘─┴┘ ┴
"""

menu["eye_candy"] = Menu(
    art_eye_candy,
    [
        Setting(
            "Caret style",
            {},
            Option(name="caret_style", options=["off", "underline", "block"]),
            info="Choose your style!",
        ),
        Setting(
            "Cursor buddy",
            {},
            NumberScroll("cursor_buddy_speed"),
            info="A cursor will race along with you with this constant speed. '0' means it will not be visible",
        ),
    ],
)

# Fifth Menu
art_misc = """
╔╦╗┬┌─┐┌─┐┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐┬ ┬┌─┐
║║║│└─┐│  ├┤ │  │  ├─┤│││├┤ │ ││ │└─┐
╩ ╩┴└─┘└─┘└─┘┴─┘┴─┘┴ ┴┘└┘└─┘└─┘└─┘└─┘
"""

menu["misc"] = Menu(
    art_misc,
    [
        Setting(
            "Tab Reset",
            {
                "on": "Pressing tab will cancel the current typing and re-start it",
                "off": "Pressing tab will have no effect ",
            },
            Option(name="tab_reset", options=["off", "on"]),
        ),
        Setting(
            "Restart Same",
            {
                "off": "Pressing tab will render a new paragraph",
                "on": "Pressing tab will restart the typing session with the same paragraph",
            },
            Option(name="restart_same", options=["off", "on"]),
        ),
        Setting(
            "Keypress Sound",
            {
                "off": "There will be no sound on keypress",
                "on": "Pressing a key will trigger a console bell except backspace",
                "backspace": "Pressing any key will trigger console bell",
            },
            Option(name="keypress_sound", options=["off", "on", "backspace"]),
        ),
    ],
)
