"""Scene is the container for all actors in the movie.

A movie can contain multiple scenes.
"""

import pygame
from pygame.sprite import AbstractGroup


class Scene():

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.actors = list()
        self.time = 0
        self.framerate = 60
        self.timestep = round(1/self.framerate, 4)

        pygame.init()  # TODO: find a better place to init pygame

    def set_framerate(self, fr):
        self.framerate = min(fr, 60)
        self.timestep = round(1/self.framerate, 4)

    def add_actor(self, actor):
        self.actors.append(actor)

    def update(self):
        self.time += self.timestep
        for actor in self.actors:
            actor.update(self.time)

    def draw(self):
        self.screen.fill(0)
        blit_args = [(a.image, a.rect) for a in self.actors]
        self.screen.blits(blit_args)
        pygame.display.flip()
