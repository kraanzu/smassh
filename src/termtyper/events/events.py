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


class UpdateRaceHUD(Message, bubble=True):
    """
    An Event Class to continously update the Race HUD
    """

    def __init__(self, sender: MessageTarget, completed: float, speed: float, accuracy: float) -> None:
        super().__init__(sender)
        self.completed = completed
        self.speed = speed
        self.accuracy = accuracy


class ResetHUD(Message, bubble=True):
    """
    An Event Class to reset the HUD
    """

    pass
