from typing import Literal
from textual.app import App
from textual.widget import Widget


class Screen(Widget):
    def __init__(
        self,
        paragraph: str,
        speed_threshold: int | None = None,
        accuracy_threshhold: int | None = None,
        cursor_buddy_speed: int | None = None,
        force_correct: bool = False,
        tab_reset: bool = False,
        difficulty: Literal["normal", "expert", "master"] = "normal",
        repeat_same: bool = False,
        blind_mode: bool = False,
        single_line_words: bool = False,
        sound: bool = False,
        caret_style: Literal["underline", "block", "off"] = "off",
    ):
        self.paragraph = paragraph
        self.speed_threshold = speed_threshold
        self.accuracy_threshhold = accuracy_threshhold
        self.cursor_buddy_speed = cursor_buddy_speed
        self.force_correct = force_correct
        self.tab_reset = tab_reset
        self.difficulty = difficulty
        self.repeat_same = repeat_same
        self.blind_mode = blind_mode
        self.single_line_words = single_line_words
        self.sound = sound
        self.caret_style = caret_style


if __name__ == "__main__":

    class MyApp(App):
        async def on_mount(self):
            self.x = Screen("hi")
            await self.view.dock(self.x)

    MyApp.run()
