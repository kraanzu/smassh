from rich.align import Align
from rich.panel import Panel
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


def colored(text: str, color: str) -> str:
    return f"[{color}]{text}[/{color}]"


seperator = f"{colored('─' * 50, 'bold dim black')}"


GETTING_STARTERD_MESSAGE = f"""
{colored(f'''
Termtyper is a TUI typing application which was highly inspired
by monekytpe -- An online web-based typing application which is
by far the most customizable typing application

Termtyper tries to bring features of monkeytype to terminal
and maybe more? who knows :p'''
, "orange1")}

{seperator}


The UI is pretty straightforward, you can start typing
or can tweak settings from the `settings` options in main-menu.
You will get a detailed description of each settings there :)

{colored("Note:", "yellow")}
If you need any help regarding settings...
press {colored("ctrl+h", "bold blue")} once in the setting menu

{seperator}

Some basic keybindings while in typing space:

 - pressing {colored("ctrl+z", "bold blue")} will toggle race-bar details

 - pressing {colored("ctrl+b", "bold blue")} will open up a bar theme menu

 - pressing {colored("ctrl+s", "bold blue")} will open ap a size/time change menu

 - pressing {colored("ctrl+o", "bold blue")} will open up a mode change menu

 - pressing {colored("ctrl+w", "bold blue")} will delete a whole word
 eg:

     {colored("This is h", "green")}{colored("ello", "red")}{colored("W", "reverse")}orld

     after pressing {colored("ctrl+w", "bold blue")}:
     {colored("This is", "green")} {colored("h", "reverse")}elloWorld

{seperator}

 - pressing {colored("ctrl+l", "bold blue")} will delete a whole line
 eg:

     {colored("This is first line. This is h", "green")}{colored("ello", "red")}{colored("W", "reverse")}orld

     after pressing {colored("ctrl+l", "bold blue")}:
     {colored("This is first line.", "green")} {colored("T", "reverse")}his is helloWorld

Also, you can exit the application by pressing {colored("ctrl+q", "bold blue")} :)

{seperator}
{seperator}

           {colored("I hope you like my little project :heart:", "plum2")}

                    -- {colored("kraanzu", "medium_purple1")}
"""
