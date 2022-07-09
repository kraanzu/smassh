from textual.message import Message, MessageTarget


class ButtonSelect(Message, bubble=True):
    """
    An Event class for when the Button is clicked
    """

    pass


class BarThemeChange(Message, bubble=True):
    """
    An Event class for when the size is changed
    """

    def __init__(self, sender: MessageTarget, theme: str | None = None) -> None:
        super().__init__(sender)
        self.theme = theme


class ParaSizeChange(Message, bubble=True):
    """
    An Event class for when the size is changed
    """

    def __init__(self, sender: MessageTarget, length: str | None = None) -> None:
        super().__init__(sender)
        self.length = length


class ModeChange(Message, bubble=True):
    """
    An Event class for when the size is changed
    """

    def __init__(self, sender: MessageTarget, mode: str | None = None) -> None:
        super().__init__(sender)
        self.mode = mode


class TimeoutChange(Message, bubble=True):
    """
    An Event class for when the size is changed
    """

    def __init__(self, sender: MessageTarget, time: str | None = None) -> None:
        super().__init__(sender)
        self.time = time


class ButtonClicked(Message, bubble=True):
    """
    An Event class for when the Button is clicked
    """

    def __init__(self, sender: MessageTarget, value: str | None = None) -> None:
        super().__init__(sender)
        self.value = value


class UpdateRaceHUD(Message, bubble=True):
    """
    An Event Class to continously update the Race HUD
    """

    def __init__(
        self, sender: MessageTarget, completed: float, speed: float, accuracy: float
    ) -> None:
        super().__init__(sender)
        self.completed = completed
        self.speed = speed
        self.accuracy = accuracy


class LoadScreen(Message, bubble=True):
    """
    An Event class to load the wanted screen
    """

    def __init__(self, sender: MessageTarget, screen: str) -> None:
        super().__init__(sender)
        self.screen = screen

    pass


class ResetHUD(Message, bubble=True):
    """
    An Event Class to reset the HUD
    """

    pass
