from __future__ import annotations

from collections import deque

import abc
import random


class Architecture:

    def __init__(self) -> None:
        self.generators = []
        self.construction_state = {
            "areas": 0,
            "connections": 0,
            "decorators": [],
            "styles": [],
            "progress": 0,
            }

        # NOTE: To do 'progress' - get the count of all tasks in all generators
        # number of completed tasks / total tasks = progress

    def add_generator(self, generator) -> None:
        self.generators.append(generator)


class Controller:

    def __init__(self, architecture: Architecture) -> None:
        self.architecture = architecture

    def loop(self) -> Architecture:
        while self.architecture.construction_state['progress'] < 100:
            for generator in self.architecture.generators:
                if generator.has_tasks:
                    generator.generate()
        decorators = self.architecture.construction_state['decorators']
        styles = self.architecture.construction_state['styles']
        return decorators, styles


class AbstractArchitect(metaclass=abc.ABCMeta):

    def __init__(self, architecture: Architecture) -> None:
        self.architecture = architecture

    @property
    @abc.abstractmethod
    def has_tasks(self):
        raise NotImplementedError("Must provide implementation in subclass.")

    @abc.abstractmethod
    def generate(self):
        raise NotImplementedError("Must provide implementation in subclass.")


class ShopArchitect(AbstractArchitect):

    tasks = deque([])

    def __init__(self, workspace) -> None:
        self.workspace = workspace

    @property
    def has_tasks(self):
        if len(self.tasks) > 0:
            return True

    def perform_task(self):
        task = self.tasks.popleft()
        return task(self.workspace)
