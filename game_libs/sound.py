import os
import sys

import pygame

from game_libs.constants import Constants


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return base_path + relative_path


pygame.mixer.init()
vol = Constants.VOLUME
sound_fx = {"hammer": pygame.mixer.Sound(resource_path(r"\assets\sound_fx\hammer.wav")),
            'moo1': pygame.mixer.Sound(resource_path(r"\assets\sound_fx\moo1.wav"))}

for sound in sound_fx.values():
    sound.set_volume(vol)
