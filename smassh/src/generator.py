import operator
import textwrap
from json import load
from itertools import accumulate
from collections.abc import Callable
from typing import List
from smassh.src.parser import config_parser
from random import randint, choice, sample


PUNCS = ",.;?!"
GeneratorFunc = Callable[..., str]


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

        if not config_parser.get("punctuations"):
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


def capitalization(func: GeneratorFunc) -> GeneratorFunc:
    def wrapper(*args, **kwargs):
        paragraph = func(*args, **kwargs)

        if config_parser.get("capitalization_mode") == "off":
            return paragraph

        def convert(word: str) -> str:
            if config_parser.get("capitalization_mode") == "on":
                return word[0].upper() + word[1:]

            return "".join([i.upper() if randint(0, 1) else i for i in word])

        words = paragraph.split()
        new_paragraph = []

        for word in words:
            i = randint(0, 2)
            if i == 0:
                word = convert(word)

            new_paragraph.append(word)

        return " ".join(new_paragraph)

    return wrapper


class Generator:
    """
    Generator class to generate paragraphs for typing tests
    """

    def __init__(self) -> None:
        self.settings = {}

    def get_words(self, language: str) -> List[str]:
        from smassh.src.parser.data_parser import DataParser

        path = DataParser.lang_path / f"{language}.json"
        with open(path) as f:
            return load(f)["words"]

    @capitalization
    @punctuations
    @numbers
    def generate(self, language: str, size: int) -> str:
        words = self.get_words(language)

        if size > len(words):
            q = size // len(words)
            words = words * q + words[: size % len(words)]

        return " ".join(sample(words, size))

    def get_newlines(self, paragraph: str, width: int) -> List[int]:
        lines = textwrap.wrap(paragraph, width)
        return list(
            accumulate(
                [len(line) + 1 for line in lines],
                operator.add,
            )
        )


master_generator = Generator()
