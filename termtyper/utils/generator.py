from pathlib import Path
from random import choice, random, randint

WORD_FILE = Path(__file__).parent / "txt" / "words.txt"
PUNCS = "$%&'(),-.:;?"
with open(WORD_FILE, "r") as f:
    words = f.read().splitlines()


def generate(times: int = 1, numbers: bool = False, punctuations: bool = False, capitalizitions: str = "off") -> str:
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
            match capitalizitions:
                case "on":
                    if random() > 0.7:
                        i = i.capitalize()
                case "max":
                    r = random()
                    if r > 0.7:
                        i = i.capitalize()
                    elif r > 0.6:
                        i = i.upper()
                    elif r > 0.4:
                        upper_indexs = [randint(0, len(i) - 1) for _i in range(randint(1, len(i)))]
                        for index in upper_indexs:
                            i = i[:index] + i[index].upper() + i[index + 1:]
                case _:
                    pass
            para += " " + i

    return para.strip()
