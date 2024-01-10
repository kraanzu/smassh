from collections.abc import Callable
from termtyper.assets.words import *  # noqa
from termtyper.src.parser import config_parser
from random import randint, choice, sample


PUNCS = ",.;?!"
GeneratorFunc = Callable[["Generator"], str]


def numbers(func: GeneratorFunc) -> GeneratorFunc:
    def wrapper(*args, **kwargs):
        paragraph = func(*args, **kwargs)

        if not config_parser.get("numbers"):
            return paragraph

        words = paragraph.split()
        total_words = len(words)
        words_to_insert = total_words // 5
        positions = sample(range(total_words), words_to_insert)
        positions.sort()

        for position in positions:
            numbers = [str(randint(10**i, 10 ** (i + 1))) for i in range(4)]
            words[position] = choice(numbers)

        return " ".join(words)

    return wrapper


def punctuations(func: GeneratorFunc) -> GeneratorFunc:
    def wrapper(*args, **kwargs):
        paragraph = func(*args, **kwargs)

        if config_parser.get("punctuations"):
            return paragraph

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

        return " ".join(new_paragraph)

    return wrapper


class Generator:
    def __init__(self) -> None:
        self.settings = {}

    @property
    def words(self) -> str:
        return " ".join(sample(english_words.split(), 64))

    @numbers
    @punctuations
    def generate(self) -> str:
        return self.words


master_generator = Generator()
