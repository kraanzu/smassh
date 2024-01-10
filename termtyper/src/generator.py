from collections.abc import Callable
from termtyper.assets.words import *  # noqa
from termtyper.src.parser import config_parser
from random import randint, choice, sample


PUNCS = ",.;?!"
GeneratorFunc = Callable[["Generator"], str]


def punctuations(func: GeneratorFunc) -> GeneratorFunc:
    def wrapper(*args, **kwargs):
        paragraph = func(*args, **kwargs)

        if config_parser.get("punctuations"):
            words = paragraph.split()
            new_paragraph = []

            for word in words:
                i = randint(0, 20)

                if i == 0:
                    word = word + choice(PUNCS)
                elif i == 1:
                    word = f"'{word}'"
                elif i == 2:
                    word = f'"{word}"'
                elif i == 3:
                    word = f"({word})"

                new_paragraph.append(word)

            paragraph = " ".join(new_paragraph)

        return paragraph

    return wrapper


class Generator:
    def __init__(self) -> None:
        self.settings = {}

    @property
    def words(self) -> str:
        return " ".join(sample(english_words.split(), 64))

    @punctuations
    def generate(self) -> str:
        return self.words


master_generator = Generator()
