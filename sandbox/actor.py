from enum import Enum
import pygame

class Actor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.actions = list()

    def update(self, time):
        self.time

class Action():

    class Act(Enum):
        STOP = 0
        MOVE = 1

    def __init__(self, start=0, end=0, action=Act.STOP):
        self.start = start
        self.end = end
        self.action = action
