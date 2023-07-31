"""
This file is to generate not too big figlet form of letters (soon digits)
"""

from typing import List


LETTERS = {
    "a": [
        "┏┓",
        "┣┫",
        "╹╹",
    ],
    "b": [
        "┏┓",
        "┣┫",
        "┗┛",
    ],
    "c": [
        "┏╸",
        "┃ ",
        "┗╸",
    ],
    "d": [
        "┏┓",
        "┃┃",
        "┗┛",
    ],
    "e": [
        "┏╸",
        "┣╸",
        "┗╸",
    ],
    "f": [
        "┏╸",
        "┣╸",
        "╹ ",
    ],
    "g": [
        "┏╸",
        "┃┓",
        "┗┛",
    ],
    "h": [
        "╻╻",
        "┣┫",
        "╹╹",
    ],
    "i": [
        "╻",
        "┃",
        "╹",
    ],
    "j": [
        "╺┓",
        " ┃",
        "┗┛",
    ],
    "k": [
        "╻┏╸",
        "┃┫ ",
        "╹┗╸",
    ],
    "l": [
        "╻ ",
        "┃ ",
        "┗╸",
    ],
    "m": [
        "┏┳┓",
        "┃┃┃",
        "╹ ╹",
    ],
    "n": [
        "┏┓",
        "┃┃",
        "╹╹",
    ],
    "o": [
        "┏┓",
        "┃┃",
        "┗┛",
    ],
    "p": [
        "┏┓",
        "┣┛",
        "╹ ",
    ],
    "q": [
        "┏┓",
        "┃┃",
        "┗┻",
    ],
    "r": [
        "┏┓",
        "┣┫",
        "╹┗",
    ],
    "s": [
        "┏╸",
        "┗┓",
        "╺┛",
    ],
    "t": [
        "╺┳╸",
        " ┃ ",
        " ╹ ",
    ],
    "u": [
        "╻╻",
        "┃┃",
        "┗┛",
    ],
    "v": [
        "┓┏",
        "┃┃",
        "┗┛",
    ],
    "w": [
        "╻ ╻",
        "┃┃┃",
        "┗┻┛",
    ],
    "x": [
        "╺┓┏╸",
        " ┃┃ ",
        "╺┛┗╸",
    ],
    "y": [
        "╻╻",
        "┗┫",
        " ┛",
    ],
    "z": [
        "┏┓",
        "┏┛",
        "┗┛",
    ],
}

COMBO = LETTERS

FigletType = List[str]


def combine_figlets(figlets: List[FigletType]) -> str:
    res = []
    for line in range(3):
        temp = ""
        for figlet in figlets:
            temp += figlet[line]

        res.append(temp)

    return "\n".join(res)


def generate_figlet(phrase: str) -> str:
    phrase = phrase.lower()
    figlets = [COMBO[letter] for letter in phrase]
    return combine_figlets(figlets)
