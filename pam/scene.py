"""Scene is the container for all actors in the movie.

A movie can contain multiple scenes.
"""

from decimal import Decimal, ROUND_HALF_UP
from pygame.sprite import AbstractGroup


class Scene(AbstractGroup):

    def __init__(self):
        super().__init__()
        self.actors = list()
        self.time = 0
        self.framerate = 60
        self.timestep = round(1/self.framerate, 4)

    def set_framerate(self, fr):
        self.framerate = fr
        self.timestep = round(1/self.framerate, 4)

    def add_actor(self, actor):
        self.actors.append(actor)

    def update(self):
        self.time += self.timestep
        for actor in self.actors:
            actor.update(self.time)
