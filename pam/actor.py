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

        self._rect = None
        self._pos = (0, 0)
        self._color = (255, 255, 255)
        self._angle = 0

        self.image = None
        self.rect = (0, 0, width, height)
        self.position = (0, 0)

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, pos):
        self._pos = pos
        self.rect.topleft = pos
        self.actions.init_states({"position": pos})

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, r):
        left, top, width, height = r
        self._pos = (left, top)
        self._rect = pygame.Rect(left, top, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c
        self.image.fill(c)
        self.actions.init_states({"color": c})

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, a):
        self._angle = a
        self.actions.init_states({"angle": a})

    def act(self, action, duration=0, dest=""):
        self.actions.add_action(action, duration, dest)

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
