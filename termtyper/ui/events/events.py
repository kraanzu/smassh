from textual.message import Message


class SetScreen(Message):
    def __init__(self, screen_name: str) -> None:
        super().__init__()
        self.screen_name = screen_name
