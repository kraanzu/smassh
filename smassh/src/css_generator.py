from appdirs import user_cache_dir
from pathlib import Path

TARGET_FOLDER = Path(user_cache_dir("smassh"))
TARGET_FILE = TARGET_FOLDER / "styles.tcss"


def write_css_file(theme_css: str, base_css: str) -> None:
    if not TARGET_FILE.exists():
        TARGET_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(TARGET_FILE, "w") as target:
        target.write(theme_css)
        target.write(base_css)


def generate_theme_file(theme: str) -> None:
    """
    Theme generator which merges theme and base CSS files

    Args:
        theme (str): theme name
    """

    css_folder = Path.absolute(Path(__file__).parent.parent) / "ui" / "css"
    themes_folder = css_folder / "themes"

    base_path = css_folder / "base.tcss"
    theme_path = themes_folder / f"{theme}.tcss"

    with open(theme_path, "r") as theme_file:
        theme_css = theme_file.read()

    with open(base_path, "r") as base_file:
        base_css = base_file.read()

    write_css_file(theme_css, base_css)
