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
            'moo1': pygame.mixer.Sound(resource_path(r"\assets\sound_fx\moo1.wav")),
            'denied': pygame.mixer.Sound(resource_path(r"\assets\sound_fx\denied.wav"))}

sound_fx['hammer'].set_volume(vol)
sound_fx['moo1'].set_volume(vol)
sound_fx['denied'].set_volume(vol * 4)
