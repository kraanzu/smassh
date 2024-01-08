from time import time
from dataclasses import dataclass
from enum import Enum


class Match(Enum):
    MATCH = 1
    MISMATCH = 2
    BACKSPACE = 3


@dataclass
class CheckPoint:
    position: int
    correct: Match

    def add_elapsed(self, elapsed) -> None:
        self.elapsed = elapsed


class StatsTracker:
    def __init__(self) -> None:
        self.reset()

    @property
    def raw_wpm(self) -> float:
        ...

    @property
    def accuracy(self) -> float:
        ...

    @property
    def wpm(self) -> float:
        ...

    @property
    def correct(self) -> int:
        ...

    @property
    def incorrect(self) -> int:
        ...

    @property
    def missed(self) -> int:
        ...

    # ---------------------------------------

    def reset(self) -> None:
        self.start_time = None
        self.end_time = None
        self.checkpoints = []

    def add_checkpoint(self, checkpoint: CheckPoint) -> None:
        if not self.start_time:
            self.start_time = time()

        elapsed = time() - self.start_time
        checkpoint.add_elapsed(elapsed)

        self.checkpoints.append(checkpoint)