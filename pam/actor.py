"""Actor object for the movie

Actor is the basic building block of the movie. Anything dynamic in the movie
should be an actor
"""

from enum import Enum
import pygame


class Act(Enum):
    """Action type for actors"""

    STOP = 0
    MOVE = 1
    ROTATE = 2
    ANIMATE = 3
    CHANGE_ATTR = 4


class Actor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.actions = Actions()

    def add_action(self, action, duration=0, dest=""):
        self.actions.add_action(action, duration, dest)

    def actions_count(self):
        return self.actions.actions_count()

    def action_at(self, time):
        return self.actions.at(time)


class Actions():

    class Action():

        def __init__(self, action, duration=0, dest=""):
            self.type = action
            self.duration = duration
            self.dest = dest

    def __init__(self):
        self.actions = list()
        last_act = Actions.Action(Act.STOP, 0)
        self.actions.append(last_act)

    def add_action(self, action, duration=0, dest=""):
        new_act = Actions.Action(action, duration, dest)
        self.actions.insert(-1, new_act)

    def actions_count(self):
        return len(self.actions)

    def at(self, time):
        cumm_time = 0
        for act in self.actions:
            cumm_time += act.duration
            if cumm_time > time:
                break
        return act

    def __getitem__(self, idx):
        return self.actions[idx]
