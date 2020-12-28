"""Base class definitions for actor AI."""

from __future__ import annotations
from typing import Tuple, List, Optional

import random

import numpy as np
import tcod.path

from action import Action, Impossible
from actions import common
from behavior import Behavior
from actor import Actor


class PathTo(Action):
    """Try to path towards a target."""

    def __init__(self, actor: Actor, dest_xy: Tuple[int, int]) -> None:
        super().__init__(actor)
        self.subaction: Optional[Action] = None
        self.dest_xy = dest_xy
        self.path_xy: List[Tuple[int, int]] = self.compute_path()

    def compute_path(self) -> List[Tuple[int, int]]:
        map_ = self.actor.location.area
        walkable = np.copy(map_.tiles["move_cost"])
        blocker_pos = [e.location.ij for e in map_.actors]
        blocker_index = tuple(np.transpose(blocker_pos))
        walkable[blocker_index] = 50
        walkable.T[self.dest_xy] = 1
        graph = tcod.path.SimpleGraph(cost=walkable, cardinal=2, diagonal=3)
        pf = tcod.path.Pathfinder(graph)
        pf.add_root(self.actor.location.ij)
        return [(ij[1], ij[0]) for ij in pf.path_to(self.dest_xy[::-1])[1:].tolist()]

    def plan(self) -> Action:

        if not self.path_xy:
            raise Impossible("End of path reached.")
        self.subaction = common.MoveStart(self.actor, self.path_xy[0]).plan()
        return self

    def act(self) -> None:

        assert self.subaction
        self.subaction.act()
        if self.path_xy[0] == self.actor.location.xy:
            self.path_xy.pop(0)


class BasicNPC(Behavior):
    """Base class for defining an NPC's behaviors."""

    def plan(self: BasicNPC) -> Action:
        owner = self.actor
        area = owner.location.area.area_model
        if area.visible[owner.location.ij]:
            pass
        x = random.randint(0, 1)
        y = random.randint(0, 1)
        x_neg = random.randint(0, 100)
        y_neg = random.randint(0, 100)

        if x_neg < 50:
            x = -x
        if y_neg < 50:
            y = -y

        try:
            roll = random.randint(0, 100)
            if roll < 30:
                return common.MoveStart(owner, (x, y)).plan()
            else:
                return common.MoveStart(owner, (0, 0)).plan()
        except Impossible:
            return common.MoveStart(owner, (0, 0)).plan()
