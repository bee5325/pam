"""Actor object for the movie

Actor is the basic building block of the movie. Anything dynamic in the movie
should be an actor
"""

import pygame
from pam.action import Actions


class Actor(pygame.sprite.Sprite):

    def __init__(self, width=0, height=0):
        super().__init__()
        self.actions = Actions()
        self.time = 0
        self.position = (0, 0)

        self._rect = None
        self.image = None
        self.rect = (0, 0, width, height)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, r):
        left, top, width, height = r
        self._rect = pygame.Rect(left, top, width, height)
        self.image = pygame.Surface((width, height))

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


class ActorGroup(pygame.sprite.AbstractGroup):
    # For now just so that the client code do not need to dependent on pygame.
    # In the future, see if extra functionalities is needed
    pass
