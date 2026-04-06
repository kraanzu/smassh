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
    max_lines = max((len(f) for f in figlets), default=0)
    for line in range(max_lines):
        temp = ""
        for figlet in figlets:
            if line < len(figlet):
                temp += figlet[line]
            else:
                temp += " "

        res.append(temp)

    return "\n".join(res)


def generate_figlet(phrase: str) -> str:
    phrase = phrase.lower()
    figlets = [COMBO[letter] for letter in phrase]
    return combine_figlets(figlets)
