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
        self.last_timer = 0
        self.time = 0
        self.framerate = 60
        self.timestep = round(1/self.framerate, 4)
        self.ended = False
        self._running = False
        self.running = False

        pygame.init()  # TODO: find a better place to init pygame

    @property
    def actors(self):
        return [actor for group in self.groups.values() for actor in group]

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, run):
        self._running = run
        if run:
            self.last_timer = pygame.time.get_ticks()

    def control(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type == pygame.KEYUP and
                                              event.key == pygame.K_q)):
                self.ended = True
            elif (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
                self.running = not self.running

    def set_framerate(self, fr):
        self.framerate = min(fr, 60)
        self.timestep = round(1/self.framerate, 4)

    def add_actors(self, actors, groupname="unnamed"):
        self.groups[groupname].add(actors)

    def add_actorgroup(self, group, groupname):
        if groupname in self.groups.keys():
            raise ValueError("Group {} already exists!".format(group))
        self.groups[groupname] = group

    def run(self):
        self.running = True
        while not self.ended:
            self.control()
            if self.running:
                self.update()
                self.draw()

    def sync(self):
        longest_time = max(actor.actions.end_time for actor in self.actors)
        for actor in self.actors:
            if actor.actions.end_time < longest_time:
                actor.act(ActStop, longest_time-actor.actions.end_time)

    def update(self):
        if self.running:
            # control framerate
            timediff = (pygame.time.get_ticks() - self.last_timer) / 1000
            if timediff < self.timestep:
                pygame.time.delay(int((self.timestep-timediff)*1000))

            self.time += (pygame.time.get_ticks() - self.last_timer) / 1000
            self.last_timer = pygame.time.get_ticks()
            for group in self.groups.values():
                group.update(self.time)

    def draw(self):
        self.screen.fill(0)
        for group in self.groups.values():
            group.draw(self.screen)
        pygame.display.flip()
