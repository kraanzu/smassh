from rich.align import Align
from textual.widgets import Static


def percent(part, total):
    return int(part * total / 100)


def prettier(help_menu) -> str:
    message = ""
    for help in help_menu:
        message = (
            message
            + "\n"
            + f"[bold blue]{help['title']}:[/bold blue]"
            + "\n"
            + f"[bold yellow]{help['subject']}[/bold yellow]"
            + "\n"
            + "\n"
        )

    message += "     [bold magenta]press ctrl+h/escape to quit[/bold magenta]"

    return message


HELP_MENU = [
    {
        "title": "Navigate between different settings",
        "subject": "  - Use j/down to move to next setting"
        + "\n"
        + "  - Use k/up for move to previous setting",
    },
    {
        "title": "Navigate between different options",
        "subject": "  - Use [bold]tab[/bold] to move to next option"
        + "\n"
        + "  - Use [bold]shift+tab[/bold] to move to previous option",
    },
]

HELP_MESSAGE = Static(
    Align.center(prettier(HELP_MENU)),
)
