from typing import Union
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from ..widgets.option import Option, NumberScroll

Options = Union[Option, NumberScroll]


class Setting(Widget):
    """
    A class that holds one setting for the termtyper!
    """

    DEFAULT_CSS = """
    Setting {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr auto;
        height: auto;
        border: blank;
    }
    """

    def __init__(
        self,
        title: str,
        items: dict[str, str],
        options: Options,
        info: str = "",
    ) -> None:
        super().__init__()
        self.title = title
        self.items = items
        self.options = options
        self.info = info
        if self.info:
            self.info += "\n"

        self.description = self.styled_description()

    def select(self):
        self.options.highlight()

    def deselect(self):
        self.options.lowlight()

    def select_next(self):
        self.options.select_next_option()

    def select_prev(self):
        self.options.select_prev_option()

    def compose(self) -> ComposeResult:
        yield Static(self.styled_description())
        yield self.options

    def styled_description(self) -> Text:
        c1 = "bold blue"
        c2 = "yellow"
        c3 = "cyan"
        return Text.from_markup(
            f"[{c1}]{self.title}[/{c1}]"
            + "\n"
            + f"[{c2}]{self.info}[/{c2}]"
            + "\n".join(
                f"[{c3}]{sub}[/{c3}]: {desc}" for sub, desc in self.items.items()
            )
        )


# First menu
menu = [
    Setting(
        "Min Speed",
        {},
        NumberScroll("min_speed"),
        info="Are you fast enough?"
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
    Setting(
        "Language",
        {},
        Option("language", options=["english", "french"]),
        "Choose the language you want the words to be generated from !",
    ),
    Setting(
        "Difficulty",
        {
            "normal": "You can type at your own accuracy",
            "expert": "Moving forward without writing the prev word correctly? YOU'RE FAILED!",
            "master": "A single incorrect press will declare you failed",
        },
        Option(
            "difficulty",
            options=["normal", "expert", "master"],
        ),
        "Where's the fun without some conditions?",
    ),
    Setting(
        "Blind Mode",
        {
            "off": "You will get to know whether you typed right or  wrong",
            "on": "Just believe your spidey sense!",
        },
        Option("blind_mode", options=["off", "on"]),
        "Have a lot of Confidence? Try this !"
        + "\n"
        + "Note: You should turn [bold]force correct[/bold] off if you are turing blind mode on",
    ),
    Setting(
        "Tab Reset",
        {
            "on": "Pressing tab will cancel the current typing and re-start it",
            "off": "Pressing tab will have no effect ",
        },
        Option("tab_reset", options=["off", "on"]),
        "Lost your gusto in the middle of typing? Restart by hitting a tab!",
    ),
    Setting(
        "Restart Same",
        {
            "off": "Pressing tab will render a new paragraph",
            "on": "Pressing tab will restart the typing session with the same paragraph",
        },
        Option("restart_same", options=["off", "on"]),
        "Wanna practice the same paragraph over and over? This option is for you!",
    ),
    Setting(
        "Force correct",
        {
            "on": "You will not be allowed to move forward until"
            + "\n"
            + "and unless all the characters until your cursor are typed correctly",
            "off": "You live your life your own way!",
        },
        Option("force_correct", options=["off", "on"]),
        "Are you worthy?",
    ),
    Setting(
        "Confidence Mode:",
        {
            "off": "You can type backspace as many times you want",
            "on": "You will only be able to backspace until the start of the current word",
            "max": "You will not be able to press backspace at all",
        },
        Option("confidence_mode", options=["off", "on", "max"]),
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
            "capitalization_mode",
            options=["off", "on", "max"],
        ),
        "Getting your hands dirty?",
    ),
    Setting(
        "Caret style",
        {
            "off": "[green]hello pete[/green]r",
            "underline": "[green]hello pete[/green][underline]r[/underline]",
            "block": "[green]hello pete[/green][reverse]r[/reverse]",
        },
        Option(
            "caret_style",
            options=["off", "underline", "block"],
        ),
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
    Setting(
        "Keypress Sound",
        {
            "off": "Already have good switches? There will be no sound on keypress",
            "on": "Pressing a key will trigger a click sound except backspace",
            "backspace": "Pressing key, including backspace, will trigger click sound",
        },
        Option(
            "keypress_sound",
            options=["off", "on", "backspace"],
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
        ),
        "Choose whats most pleasing to you ears :)",
    ),
]