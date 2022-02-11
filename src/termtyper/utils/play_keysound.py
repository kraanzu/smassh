from ..utils import Parser
from playsound import playsound
from threading import Thread


def get_sound_location(sound: str):
    return f"./src/termtyper/sounds/{sound}.wav"


def play(sound_file):
    playsound(sound_file)


def play_keysound():
    sound = Parser().get_data("sound")
    sound_file = get_sound_location(sound)
    Thread(target=play, args=(sound_file,)).start()


def play_failed():
    sound_file = get_sound_location("failed")
    Thread(target=play, args=(sound_file,)).start()
