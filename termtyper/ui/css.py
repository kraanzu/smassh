import os
from pathlib import Path


def load_folder(folder):
    """
    Load all css files in a folder and return them as a single string
    """

    css = ""

    for file in os.listdir(folder):
        if not file.endswith(".css"):
            continue

        with open(os.path.join(folder, file), "r") as css_file:
            css += css_file.read()

    return css


CSS = ""
css_folder = Path(__file__).parent / "css"
theme_folder = css_folder / "themes"


CSS += load_folder(css_folder)
CSS += load_folder(theme_folder)
