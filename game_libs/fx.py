from random import randint

from game_libs.constants import Constants
from game_libs.sprites import Cloud


class Weather:
    """weather controller class, draws weather events at random intervals"""

    def __init__(self):
        self.clouds = [Cloud()]
        self.time_remaining = randint(2, 10) * Constants.FRAMERATE

    def reset_timer(self):
        """reset the time remaining for events"""
        self.time_remaining = randint(2, 10) * Constants.FRAMERATE

    def weather_step(self):
        """step event to be called every frame"""
        # if timer has ran to 0, create a new cloud
        if self.time_remaining > 0:
            self.time_remaining -= 1
        else:
            self.clouds.append(Cloud())
            self.reset_timer()

        # move each cloud at its individual speed and draw
        # if cloud is out of screen bounds by 200px, destroy it
        for i, cloud in enumerate(self.clouds):
            cloud.draw()
            cloud.move()
            if cloud.x - 200 > Constants.WINDOW_WIDTH:
                self.clouds.pop(i)
