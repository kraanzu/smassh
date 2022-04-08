from textual.message import Message, MessageTarget


class ButtonSelect(Message, bubble=True):
    """
    An Event class for when the Button is clicked
    """

    pass


class ButtonClicked(Message, bubble=True):
    """
    An Event class for when the Button is clicked
    """

    pass


class UpdateRaceBar(Message, bubble=True):
    """
    An Event Class to continously update the Race Bar
    """

    def __init__(self, sender: MessageTarget, completed: float, speed: float) -> None:
        super().__init__(sender)
        self.completed = completed
        self.speed = speed


class ResetBar(Message, bubble=True):
    """
    An Event Class to reset the bar
    """

    pass
