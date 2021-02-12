from __future__ import annotations

import abc
import random
from collections import deque
from typing import TYPE_CHECKING, Tuple, List, Type

import numpy as np
from simulacra.core.options import *
from simulacra.utils.geometry import Rect, Point

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager
    from simulacra.world.area import Area


class Workspace:

    def __init__(self, manager: AreaManager) -> None:
        """Procedural Generation Workspace

        Implementation of the `Blackboard` pattern representing a shared construction
        state that results in a generated game area. It calls specific Architects to
        manage and complete tasks for sub-tasks in the generation process.

        The cumulative result is represented as a `progress` entry in the shared
        construction state.
        """
        self.manager = manager
        self.shape = (STAGE_WIDTH, STAGE_HEIGHT)
        self.architects = []
        self.construction_state = {
            "passable": np.ones(self.shape, dtype=np.bool, order="F"),
            "transparent": np.zeros(self.shape, dtype=np.bool, order="F"),
            "owner_uids": np.zeros(self.shape, dtype=np.int32, order="F"),
            "architects": [],
            "progress": 0,
            }

    def add_architect(self, architect: Type[AbstractArchitect]) -> None:
        self.architects.append(architect)


class Controller:

    def __init__(self, workspace: Workspace) -> None:
        """Controller class for running the actual procedural generation process.

        The Workspace is a single area that is the current focus of the generation
        system. Architect subclasses are called to contribute subcomponents of the area.
        """
        self.workspace = workspace
        self.architect_uid = 0

    def loop(self) -> List[Type[AbstractArchitect]]:
        while self.workspace.construction_state['progress'] < 100:
            for architect in self.workspace.architects:
                architect = architect(self.workspace)

                self.architect_uid += 1
                architect.uid = self.architect_uid

                if architect.has_tasks:
                    architect.perform_tasks()

        return self.workspace['architects']


class Task(metaclass=abc.ABCMeta):

    def __init__(self, workspace: Workspace) -> None:
        self.workspace = workspace

    @abc.abstractmethod
    def perform(self) -> Workspace:
        raise NotImplementedError

    @property
    def result(self):
        return self.workspace


class AbstractArchitect(metaclass=abc.ABCMeta):

    def __init__(self, workspace: Workspace) -> None:
        """An Architect is a delegator of a higher procedural generation process.
        Each Architect has a queue of tasks that must be performed. An Architect
        takes in the active workspace and sets a region of the workspace as its
        'owned' area. It then iteratively delegates tasks to various worker
        objects that modify the owned area.
        """
        self.tasks = deque([])
        self.workspace = workspace
        self.uid = 0

    @property
    @abc.abstractmethod
    def has_tasks(self):
        raise NotImplementedError("Must provide implementation in subclass.")

    @abc.abstractmethod
    def perform_tasks(self):
        raise NotImplementedError("Must provide implementation in subclass.")

    def add_task(self, task: Task):
        self.tasks.append(task)


class ShopArchitect(AbstractArchitect):

    @property
    def has_tasks(self):
        if len(self.tasks) > 0:
            return True

    def perform_tasks(self):
        while self.has_tasks:
            task = self.tasks.popleft()
            task(self.workspace)
            task.perform()
            yield task.result


class Painter:

    def __init__(self, workspace: Workspace) -> None:
        self.workspace = workspace
        self._manager = self.workspace.manager
        self.decoration_state = {
            "saturated": np.zeros(self.shape, dtype=object, order="F"),
            "desaturated": np.zeros(self.shape, dtype=object, order="F"),
            "progress": 0,
            }


if __name__ == '__main__':
    print("Running Architect")
