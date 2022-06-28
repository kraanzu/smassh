from pathlib import Path
from random import choice

WORD_FILE = Path(__file__).parent / "txt" / "words.txt"
with open(WORD_FILE, "r") as f:
    words = f.read().splitlines()


def generate(times: int = 1) -> str:
    """
    produces a paragraph
    """
    times *= 50
    return " ".join([choice(words) for _ in " " * times])
