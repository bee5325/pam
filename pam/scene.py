"""Scene is the container for all actors in the movie.

A movie can contain multiple scenes.
"""

from enum import Enum
from collections import defaultdict
import pygame
from pam.actor import ActorGroup
from pam.action import ActStop


class PlayDir(Enum):
    """Enum for play direction, either forward or backward"""

    FORWARD = 0
    BACKWARD = 1


class Scene():

    def __init__(self, width, height):
        super().__init__()
        self.screen = pygame.display.set_mode((width, height))
        self.groups = defaultdict(ActorGroup)
        self._last_timer = 0
        self._time = 0
        self._framerate = 60
        self._timestep = round(1/self._framerate, 4)
        self._ended = False
        self._running = False
        self._direction = PlayDir.FORWARD

        self.running = False
        self.framerate = 60

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
            self._last_timer = pygame.time.get_ticks()

    @property
    def end_time(self):
        return max((actor.actions.end_time for actor in self.actors),
                   default=0)

    def add_actors(self, actors, groupname="unnamed"):
        """Adding actors to the scene

        Args:
            actors (Actor): Single actor or iterable of actors to be added
            groupname (str, optional): groupname for the actors to be added.
                Default to "unnamed"
        """

        self.groups[groupname].add(actors)

    def add_actorgroup(self, group, groupname):
        if groupname in self.groups.keys():
            raise ValueError("Group {} already exists!".format(group))
        self.groups[groupname] = group

    def sync(self):
        for actor in self.actors:
            if actor.actions.end_time < self.end_time:
                actor.act(ActStop, self.end_time-actor.actions.end_time)

    @property
    def framerate(self):
        return self._framerate

    @framerate.setter
    def framerate(self, fr):
        self._framerate = min(fr, 60)
        self._timestep = round(1/self._framerate, 4)

    def control(self):
        """Entry point for where all controls should be done

        The available basic controls are:
            :q: Quit
            :SPACE: Pause
            :LEFT: Running backward
            :RIGHT: Running forward

        The function can be extended to provide more controls. Check
        pygame.event_ for more info

        .. _pygame.event: https://www.pygame.org/docs/ref/event.html"""

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type == pygame.KEYUP and
                                              event.key == pygame.K_q)):
                self._ended = True
            elif (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
                self.running = not self.running
            elif (event.type == pygame.KEYUP and event.key == pygame.K_LEFT):
                self._direction = PlayDir.BACKWARD
            elif (event.type == pygame.KEYUP and event.key == pygame.K_RIGHT):
                self._direction = PlayDir.FORWARD

    def run(self):
        self.running = True
        while not self._ended:
            self.control()
            if self.running:
                self.update()
                self.draw()

    def update(self):
        if self.running:
            # control framerate
            timediff = (pygame.time.get_ticks() - self._last_timer) / 1000
            if timediff < self._timestep:
                pygame.time.delay(int((self._timestep-timediff)*1000))

            if self._direction == PlayDir.FORWARD:
                self._time += (pygame.time.get_ticks()-self._last_timer) / 1000
                self._time = min(self.end_time, self._time)
            elif self._direction == PlayDir.BACKWARD:
                self._time -= (pygame.time.get_ticks()-self._last_timer) / 1000
                self._time = max(0, self._time)
            for group in self.groups.values():
                group.update(self._time)
            self._last_timer = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill(0)
        for group in self.groups.values():
            group.draw(self.screen)
        pygame.display.flip()
