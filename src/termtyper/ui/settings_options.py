from rich.text import TextType, Text
from textual.widget import Widget
from collections import OrderedDict

from ..ui.widgets import Option, NumberScroll
from ..utils import play_keysound


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
┬ ┬┌─┐┬─┐┌┬┐┌─┐┌─┐┬─┐┌─┐
├─┤├─┤├┬┘ │││  │ │├┬┘├┤
┴ ┴┴ ┴┴└──┴┘└─┘└─┘┴└─└─┘
"""
menu["hardcore"] = Menu(
    art_hardcore,
    [
        Setting(
            "Paragraph Size",
            {},
            Option(name="paragraph_size", options=["teensy", "small", "big", "huge"]),
            info="So how much can your fingers handle?",
        ),
        Setting(
            "Difficulty",
            {
                "normal": "You can type at your own accuracy",
                "expert": "Moving forward without writing the prev word correctly? YOU'RE FAILED!",
                "master": "A single incorrect press will declare you failed",
            },
            Option(name="difficulty", options=["normal", "expert", "master"]),
            "Where's the fun without some conditions?",
        ),
        Setting(
            "Blind Mode",
            {
                "off": "You will get to know whether you typed right or  wrong",
                "on": "Just believe your spidey sense!",
            },
            Option(name="blind_mode", options=["off", "on"]),
            "Have a lot of Confidence? Try this !"
            + "\n"
            + "Note: You should turn [bold]force correct[/bold] off if you are turing blind mode on",
        ),
    ],
)


# Second menu
art_push_your_limits = """
┌─┐┬ ┬┌─┐┬ ┬  ┬ ┬┌─┐┬ ┬┬─┐  ┬  ┬┌┬┐┬┌┬┐┌─┐
├─┘│ │└─┐├─┤  └┬┘│ ││ │├┬┘  │  │││││ │ └─┐
┴  └─┘└─┘┴ ┴   ┴ └─┘└─┘┴└─  ┴─┘┴┴ ┴┴ ┴ └─┘
"""
menu["push_your_limits"] = Menu(
    art_push_your_limits,
    [
        Setting(
            "Min Speed",
            {},
            NumberScroll("min_speed"),
            info="Are you lightning MCQueen?"
            + "\n"
            + "Note: If your speed falls below this speed you will be declared failed",
        ),
        Setting(
            "Min Accuracy",
            {},
            NumberScroll("min_accuracy"),
            info="You can't go wrong with this"
            + "\n"
            + "Note: If your accuracy falls below this accuracy you will be declared failed",
        ),
        Setting(
            "Min Burst:",
            {},
            NumberScroll("min_burst"),
            info="Wanna make your life harder?"
            + "\n"
            + "Note: If your accuracy for a word falls below this accuracy you will be declared failed",
        ),
    ],
)

# Third Menu
art_discipline = """
┌┬┐┬┌─┐┌─┐┬┌─┐┬  ┬┌┐┌┌─┐
 │││└─┐│  │├─┘│  ││││├┤
─┴┘┴└─┘└─┘┴┴  ┴─┘┴┘└┘└─┘
"""
menu["discipline"] = Menu(
    art_discipline,
    [
        Setting(
            "Force correct",
            {
                "on": "You will not be allowed to move forward until"
                + "\n"
                + "and unless all the characters until your cursor are typed correctly",
                "off": "You live your life your own way!",
            },
            Option(name="force_correct", options=["off", "on"]),
            "Are you worthy?",
        ),
        Setting(
            "Confidence Mode:",
            {
                "off": "You can type backspace as many times you want",
                "on": "You will only be able to backspace until the start of the current word",
                "max": "You will not be able to press backspace at all",
            },
            Option(name="confidence_mode", options=["off", "on", "max"]),
            "Feeling Lucky?",
        ),
    ],
)

# Fourth Menu
art_eye_candy = """
┌─┐┬ ┬┌─┐  ┌─┐┌─┐┌┐┌┌┬┐┬ ┬
├┤ └┬┘├┤   │  ├─┤│││ ││└┬┘
└─┘ ┴ └─┘  └─┘┴ ┴┘└┘─┴┘ ┴
"""

menu["eye_candy"] = Menu(
    art_eye_candy,
    [
        Setting(
            "Caret style",
            {
                "off": "[green]hello pete[/green]r",
                "underline": "[green]hello pete[/green][underline]r[/underline]",
                "block": "[green]hello pete[/green][reverse]r[/reverse]",
            },
            Option(name="caret_style", options=["off", "underline", "block"]),
            info="Choose your style!",
        ),
        Setting(
            "Cursor buddy",
            {},
            NumberScroll("cursor_buddy_speed"),
            info="Feeling a little lonely?"
            + "\n"
            + "A cursor will race along with you with this constant speed."
            + "\n"
            + "'0' means it will not be visible",
        ),
    ],
)

# Fifth Menu
art_aesthetics = """
┌─┐┌─┐┌─┐┌┬┐┬ ┬┌─┐┌┬┐┬┌─┐┌─┐
├─┤├┤ └─┐ │ ├─┤├┤  │ ││  └─┐
┴ ┴└─┘└─┘ ┴ ┴ ┴└─┘ ┴ ┴└─┘└─┘
"""

menu["ear_candy"] = Menu(
    art_aesthetics,
    [
        Setting(
            "Keypress Sound",
            {
                "off": "Already have good switches? There will be no sound on keypress",
                "on": "Pressing a key will trigger a click sound except backspace",
                "backspace": "Pressing any key will trigger click sound",
            },
            Option(name="keypress_sound", options=["off", "on", "backspace"]),
            "See ear candy menu for to get into the nitty gritty",
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
                callback=play_keysound,
            ),
            "Choose whats most pleasing to you ears :)",
        ),
    ],
)

# Sixth Menu
art_misc = """
┌┬┐┬┌─┐┌─┐┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐┬ ┬┌─┐
││││└─┐│  ├┤ │  │  ├─┤│││├┤ │ ││ │└─┐
┴ ┴┴└─┘└─┘└─┘┴─┘┴─┘┴ ┴┘└┘└─┘└─┘└─┘└─┘
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
            "Lost your gusto in the middle of typing? Restart by hitting a tab!",
        ),
        Setting(
            "Restart Same",
            {
                "off": "Pressing tab will render a new paragraph",
                "on": "Pressing tab will restart the typing session with the same paragraph",
            },
            Option(name="restart_same", options=["off", "on"]),
            "Wanna practice the same paragraph over and over? This option is for you!",
        ),
    ],
)
