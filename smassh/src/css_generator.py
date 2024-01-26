from pathlib import Path


def generate_theme_file(theme: str) -> None:
    """
    Theme generator which merges theme and base CSS files

    Args:
        theme (str): theme name
    """

    css_folder = Path.absolute(Path(__file__).parent.parent) / "ui" / "css"
    themes_folder = css_folder / "themes"

    base_path = css_folder / "base.css"
    theme_path = themes_folder / f"{theme}.tcss"
    target_file = css_folder / "styles.tcss"

    with open(theme_path, "r") as theme_file:
        theme_css = theme_file.read()

    with open(base_path, "r") as base_file:
        base_css = base_file.read()

    with open(target_file, "w") as target:
        target.write(theme_css)
        target.write(base_css)
