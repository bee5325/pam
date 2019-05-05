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
        self.time = 0
        self.position = (0, 0)

    def add_action(self, action, duration=0, dest=""):
        self.actions.add_action(action, duration, dest)

    def actions_count(self):
        return self.actions.count()

    def action_at(self, time):
        return self.actions.at(time)

    def update(self, time):
        self.time = time
        current_action = self.actions.at(time)
        setattr(self, current_action.attribute, current_action.current_state)


class Actions():

    class Action():

        def __init__(self, action, duration=0, dest=""):
            self.type = action
            self.duration = duration
            self.dest = dest
            self.current_state = 0

            if action == Act.MOVE:
                self.attribute = "position"
                self.start = (0, 0)
            elif action == Act.ROTATE:
                self.attribute = "angle"
            elif action == Act.STOP:
                self.attribute = "None"
            else:
                raise ValueError("Action {} is not supported".format(action))

        def update_current_state(self, time_passed):
            if self.type == Act.MOVE:
                t_ratio = time_passed/self.duration
                self.current_state = ((self.dest[0]-self.start[0]) * t_ratio,
                                      (self.dest[1]-self.start[1]) * t_ratio)

    def __init__(self):
        self.actions = list()
        last_act = Actions.Action(Act.STOP, 0)
        self.actions.append(last_act)

    def add_action(self, action, duration=0, dest=""):
        new_act = Actions.Action(action, duration, dest)
        self.actions.insert(-1, new_act)

    def count(self):
        return len(self.actions)

    def at(self, time):
        cumm_time = 0
        act = None
        for act in self.actions:
            cumm_time += act.duration
            if cumm_time > time:
                time_passed = time - cumm_time
                act.update_current_state(time_passed)
                break
        return act

    def __getitem__(self, idx):
        return self.actions[idx]
