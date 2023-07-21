from .words import english_words, french_words
from random import choice, random, randint


PUNCS = "$%&'(),-.:;?"

def generate(
    times: int = 1,
    numbers: bool = False,
    punctuations: bool = False,
    capitalizitions: str = "off",
    language: str = "english",
) -> str:
    """
    produces a paragraph
    """
    times *= 30
    extra = []
    if numbers:
        extra.extend([str(choice(range(1, 10000))) for _ in " " * 200])
    if punctuations:
        extra.extend([choice(PUNCS) for _ in " " * 200])
    
    match language:
        case "english":
            words = english_words
        case "french":
            words = french_words
        case _:
            pass
    words = words.split()

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
                        upper_indexs = [
                            randint(0, len(i) - 1) for _ in range(randint(1, len(i)))
                        ]
                        for index in upper_indexs:
                            i = i[:index] + i[index].upper() + i[index + 1 :]
                case _:
                    pass
            para += " " + i

    return para.strip()
