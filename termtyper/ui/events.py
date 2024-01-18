from textual.message import Message
from termtyper.src import StatsTracker


class SetScreen(Message):
    def __init__(self, screen_name: str) -> None:
        super().__init__()
        self.screen_name = screen_name


class ShowResults(Message):
    def __init__(self, stats: StatsTracker, failed: bool = False) -> None:
        super().__init__()
        self.stats = stats
        self.failed = failed
