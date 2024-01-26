from time import time
from dataclasses import dataclass
from enum import Enum
from typing import List


class Match(Enum):
    """
    Match enum class for character match
    """

    MATCH = 1
    MISMATCH = 2
    BACKSPACE = 3
    SKIPPED = 4


@dataclass
class CheckPoint:
    """
    Checkpoint class to maintain record of position and elapsed time at that point
    """

    letter: str
    position: int
    correct: Match

    def add_elapsed(self, elapsed) -> None:
        self.elapsed = elapsed


class StatsTracker:
    """
    Tracker class to calculate stats while typing
    """

    def __init__(self) -> None:
        self.reset()

    def get_checkpoints_last_word(self) -> List[CheckPoint]:
        checkpoints = self.checkpoints.copy()
        word_checkpoints = []

        while checkpoints and checkpoints[-1].letter == " ":
            checkpoints.pop()

        while checkpoints and checkpoints[-1].letter != " ":
            word_checkpoints.append(checkpoints.pop())

        return list(reversed(word_checkpoints))

    @property
    def elapsed_time(self) -> float:
        if not self.start_time:
            raise ValueError("Start time not set")

        if self.end_time:
            return self.end_time - self.start_time

        return time() - self.start_time

    @property
    def word_count(self) -> int:
        if not self.checkpoints:
            return 0

        return sum(checkpoint.letter == " " for checkpoint in self.checkpoints)

    @property
    def last_word_accuracy(self) -> int:
        correct = 0
        incorrect = 0

        checkpoints = self.get_checkpoints_last_word()

        if not checkpoints:
            raise ValueError("No checkpoints")

        for i in checkpoints:
            correct += i.correct == Match.MATCH
            incorrect += i.correct == Match.MISMATCH

        return round((correct / (correct + incorrect)) * 100)

    @property
    def last_word_wpm(self) -> int:
        checkpoints = self.get_checkpoints_last_word()

        if not checkpoints:
            raise ValueError("No checkpoints")

        start = checkpoints[0].elapsed
        stop = checkpoints[-1].elapsed
        elapsed = stop - start

        if elapsed == 0:
            raise ValueError("Elapsed time is 0")

        raw = 60 / elapsed
        return round(self.last_word_accuracy * raw / 100)

    @property
    def raw_wpm(self) -> int:
        # TODO: Better formula because this is not accurate

        time_taken = self.elapsed_time / 60
        return round(self.word_count / time_taken)

    @property
    def accuracy(self) -> int:
        accuracy = (self.correct / (self.correct + self.incorrect)) * 100
        return round(accuracy)

    @property
    def wpm(self) -> int:
        return round(self.raw_wpm * (self.accuracy / 100))

    @property
    def correct(self) -> int:
        return sum(checkpoint.correct == Match.MATCH for checkpoint in self.checkpoints)

    @property
    def incorrect(self) -> int:
        return sum(
            checkpoint.correct == Match.MISMATCH for checkpoint in self.checkpoints
        )

    @property
    def missed(self) -> int:
        return sum(
            checkpoint.correct == Match.SKIPPED for checkpoint in self.checkpoints
        )

    # ---------------------------------------

    def reset(self) -> None:
        self.start_time = None
        self.end_time = None
        self.checkpoints: List[CheckPoint] = []

    def finish(self) -> None:
        self.end_time = time()

    def add_checkpoint(self, checkpoint: CheckPoint) -> None:
        if not self.start_time:
            self.start_time = time()

        if checkpoint.correct == Match.BACKSPACE:
            diff = self.checkpoints[-1].position - checkpoint.position
            self.checkpoints = self.checkpoints[:-diff]
            return

        elapsed = time() - self.start_time
        checkpoint.add_elapsed(elapsed)

        self.checkpoints.append(checkpoint)
