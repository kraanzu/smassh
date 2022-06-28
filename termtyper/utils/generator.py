from pathlib import Path
from random import choice

WORD_FILE = Path(__file__).parent / "txt" / "words.txt"
PUNCS = "$%&'(),-.:;?"
with open(WORD_FILE, "r") as f:
    words = f.read().splitlines()


def generate(times: int = 1, numbers: bool = False, punctuations: bool = False) -> str:
    """
    produces a paragraph
    """
    times *= 30
    extra = []
    if numbers:
        extra.extend([str(choice(range(1, 10000))) for _ in " " * 50])
    if punctuations:
        extra.extend([choice(PUNCS) for _ in " " * 50])

    arr = [choice(words + extra) for _ in " " * times]
    para = ""
    for i in arr:
        if i in PUNCS:
            para += i
        else:
            para += " " + i

    return para.strip()
