from unittest import TestCase

from smassh.ui.screens.typing import TypingScreen


class TypingScreenKeypressesFromTextTest(TestCase):
    def test_splits_pasted_chinese_word_into_characters(self) -> None:
        self.assertEqual(TypingScreen.keypresses_from_text("中文"), ["中", "文"])

    def test_ignores_non_printable_text_characters(self) -> None:
        self.assertEqual(TypingScreen.keypresses_from_text("中\n文"), ["中", "文"])
