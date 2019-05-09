"""Actor object for the movie

Actor is the basic building block of the movie. Anything dynamic in the movie
should be an actor
"""

import pygame
from pam.action import Actions


class Actor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.actions = Actions()
        self.time = 0
        self.position = (0, 0)

    def add_action(self, action, duration=0, dest=""):
        self.actions.add_action(action, duration, dest)

    def actions_count(self):
        return len(self.actions)

    def action_at(self, time):
        return self.actions.action_at(time)

    def state_at(self, time):
        return self.actions.state_at(time)

    def update(self, time):
        self.time = time
        states = self.actions.state_at(time)
        for attrib, state in states.items():
            setattr(self, attrib, state)


