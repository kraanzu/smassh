from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.tree import Tree
from textual.widget import Widget
from textual.widgets import Static


ascii = """
┌─┐┌─┐┌┬┐┌┬┐┬┌┐┌┌─┐  ┌─┐┌┬┐┌─┐┬─┐┌┬┐┌─┐┌┬┐
│ ┬├┤  │  │ │││││ ┬  └─┐ │ ├─┤├┬┘ │ ├┤  ││
└─┘└─┘ ┴  ┴ ┴┘└┘└─┘  └─┘ ┴ ┴ ┴┴└─ ┴ └─┘─┴┘
"""

GETTING_STARTERD_BANNER = Static(
    Panel(
        Align.center(ascii),
        style="bold blue",
        border_style="bold magenta",
    )
)


def keybind(key: str, desc: str) -> str:
    return f"{colored('●', 'green')} {colored(key,'bold blue')} => {colored(desc,'b' )}"


def colored(text: str, color: str) -> str:
    return f"[{color}]{text}[/{color}]"


seperator = f"{colored('─' * 70, 'bold dim black')}"


INTRO = f"""
{colored(f'''
Termtyper is a TUI typing application which was highly inspired
by monkeytype -- An online web-based typing application which is
by far the most customizable typing application

Termtyper tries to bring features of monkeytype to terminal'''
, "orange1")}

The UI is pretty straightforward, you can start typing
or can tweak settings from the `settings` options in main-menu.
You will get a detailed description of each settings there :)
"""

KEYBINDS_HEADER = f"""
{colored("Note:", "yellow")}
If you need any help regarding settings...
press {colored("ctrl+h", "bold blue")} once in the setting menu

Some basic keybindings while in typing space:
"""

KEYBINGS = f"""

 {keybind("ctrl+d","toggle race-bar details" )}

 {keybind("ctrl+n","toggle numbers" )}

 {keybind("ctrl+p","toggle punctuations" )}

 {keybind("ctrl+b","open up a bar theme menu" )}

 {keybind("ctrl+s","open up a size/time change menu" )}

 {keybind("ctrl+o","open up a mode change menu" )}

 {keybind("ctrl+w","delete a whole word" )}

 eg:

     {colored("This is h", "green")}{colored("ello", "red")}{colored("W", "reverse")}orld

     after pressing {colored("ctrl+w", "bold blue")}:
     {colored("This is", "green")} {colored("h", "reverse")}elloWorld

"""

OUTRO = f"""
Also, you can exit the application by pressing {colored("ctrl+q", "bold blue")} :)


           {colored("I hope you like my little project :heart:", "plum2")}

                    -- {colored("kraanzu", "medium_purple1")}
"""


class GettingStarted(Widget):
    def render(self) -> RenderableType:

        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for i in [INTRO, KEYBINDS_HEADER, KEYBINGS, OUTRO]:
            tree.add(Align.center(i))
            tree.add(Align.center(seperator))

        return tree
