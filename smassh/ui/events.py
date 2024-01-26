from textual.message import Message
from smassh.src import StatsTracker


class SetScreen(Message):
    """
    Emitted to change the screen content
    """

    def __init__(self, screen_name: str) -> None:
        super().__init__()
        self.screen_name = screen_name


class ShowResults(Message):
    """
    Emitted when the typing is finished
    """

    def __init__(self, stats: StatsTracker, failed: bool = False) -> None:
        super().__init__()
        self.stats = stats
        self.failed = failed
