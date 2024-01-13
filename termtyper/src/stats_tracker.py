from time import time
from dataclasses import dataclass
from enum import Enum


class Match(Enum):
    MATCH = 1
    MISMATCH = 2
    BACKSPACE = 3
    SKIPPED = 4


@dataclass
class CheckPoint:
    key: str
    position: int
    correct: Match

    def add_elapsed(self, elapsed) -> None:
        self.elapsed = elapsed


class StatsTracker:
    def __init__(self) -> None:
        self.reset()

    @property
    def elapsed_time(self):
        if not self.start_time:
            raise ValueError("Start time not set")

        if self.end_time:
            return self.end_time - self.start_time

        return time() - self.start_time

    @property
    def raw_wpm(self) -> int:
        time_taken = self.elapsed_time / 60
        words = len(self.checkpoints) / 5

        return round(words / time_taken)

    @property
    def accuracy(self) -> int:
        accuracy = (self.correct / (self.correct + self.incorrect)) * 100
        return round(accuracy)

    @property
    def wpm(self) -> float:
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
        self.checkpoints = []

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
