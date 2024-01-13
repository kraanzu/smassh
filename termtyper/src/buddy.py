class Buddy:
    @classmethod
    def get_letters_typed(cls, elapsed: float, wpm: int, parity_constant: float) -> int:
        words_typed = elapsed * wpm
        letters_typed = words_typed / parity_constant
        return round(letters_typed)
