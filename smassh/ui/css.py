import os
from pathlib import Path

CSS = ""
EXTENSION = ".tcss"


def load_folder(folder: Path) -> str:
    """
    Load all css files in a folder and return them as a single string
    """

    css = ""

    for file in os.listdir(folder):
        if not file.endswith(EXTENSION):
            continue

        with open(os.path.join(folder, file), "r") as css_file:
            css += css_file.read()

    return css


css_folder = Path(__file__).parent / "css"
theme_folder = css_folder / "themes"


CSS += load_folder(css_folder)
CSS += load_folder(theme_folder)
