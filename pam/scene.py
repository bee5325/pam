"""Scene is the container for all actors in the movie.

A movie can contain multiple scenes.
"""

import sys
from collections import defaultdict
import pygame
from pam.actor import ActorGroup
from pam.action import ActStop


class Scene():

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.groups = defaultdict(ActorGroup)
        self.time = 0
        self.framerate = 60
        self.timestep = round(1/self.framerate, 4)
        self.start_time = pygame.time.get_ticks()

        pygame.init()  # TODO: find a better place to init pygame

    @property
    def actors(self):
        return [actor for group in self.groups.values() for actor in group]

    def control(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or (event.type == pygame.KEYUP
                        and event.key == pygame.K_q)):
                sys.exit()
            elif (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
                self.start_time = pygame.time.get_ticks()

    def set_framerate(self, fr):
        self.framerate = min(fr, 60)
        self.timestep = round(1/self.framerate, 4)

    def add_actors(self, actors, groupname="unnamed"):
        self.groups[groupname].add(actors)

    def add_actorgroup(self, group, groupname):
        if groupname in self.groups.keys():
            raise ValueError("Group {} already exists!".format(group))
        self.groups[groupname] = group

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def sync(self):
        longest_time = max(actor.actions.end_time for actor in self.actors)
        for actor in self.actors:
            if actor.actions.end_time < longest_time:
                actor.act(ActStop, longest_time-actor.actions.end_time)

    def update(self):
        # control framerate
        newtime = (pygame.time.get_ticks() - self.start_time) / 1000
        timediff = newtime - self.time
        if timediff < self.timestep:
            pygame.time.delay(int((self.timestep-timediff)*1000))

        self.time = (pygame.time.get_ticks() - self.start_time) / 1000
        for group in self.groups.values():
            group.update(self.time)

    def draw(self):
        self.screen.fill(0)
        for group in self.groups.values():
            group.draw(self.screen)
        pygame.display.flip()
