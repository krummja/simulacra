from __future__ import annotations  # type: ignore
from typing import Iterator, List, Tuple, Type, TYPE_CHECKING

import random

import numpy as np
from numpy import ndarray
import tcod

from engine.actions import ai, Action
from engine.character.player import Player
from engine.character import Character
from engine.character.neutral import *
from engine.character.hostile import *
from engine.area import *
from engine.tile import *
from engine.graphic import *
from engine.actions.ai import *
from engine.hues import COLOR
from engine.model import Model

if TYPE_CHECKING:
    from engine.actor import Actor
    from engine.location import Location
    from engine.model import Model


class Room:

    def __init__(self, x: int, y: int, width: int, height: int, max_entities: int=3) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.entities = 0
        self.max_entities = max_entities

    @property
    def outer(self) -> Tuple[slice, slice]:
        """Return the NumPy index for the whole room."""
        index: Tuple[slice, slice] = np.s_[self.x1 : self.x2, self.y1: self.y2]
        return index

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the NumPy index for the inner room area."""
        index: Tuple[slice, slice] = np.s_[
            self.x1 + 1 : self.x2 - 1, self.y1 + 1 : self.y2 - 1
        ]
        return index

    @property
    def center(self) -> Tuple[slice, slice]:
        """Return the index for the room's center coordinate."""
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def intersects(self, other: Room) -> bool:
        """Return True if this room intersects with another."""
        return (
            self.x1 <= other.x2 and
            self.x2 >= other.x1 and
            self.y1 <= other.y2 and
            self.y2 >= other.y1
        )

    def distance_to(self, other: Room) -> float:
        """Return an approximate distance from this room to another."""
        x, y = self.center
        other_x, other_y = other.center
        return abs(other_x - x) + abs(other_y - y)

    def get_free_spaces(
            self,
            area: Area, 
            number: int
        ) -> Iterator[Tuple[int, int]]:
        """Iterate over the x,y coordinates up to `number` spaces."""
        for _ in range(number):
            x = random.randint(self.x1 + 1, self.x2 - 2)
            y = random.randint(self.y1 + 1, self.y2 - 2)
            if area.is_blocked(x, y):
                continue
            yield x, y

    def place_npcs(self, area: Area) -> None:
        """Spawn neutral NPCs within this room."""
        npcs = random.randint(0, 3)
        items_spawned = random.randint(0, 2)
        for xy in self.get_free_spaces(area, npcs):
            monster_cls: Type[Character]
            monster_cls = NPC
            monster_cls.spawn(area[xy])
            self.entities += 1

    def place_hostiles(self, area: Area) -> None:
        """Spawn hostile NPCs within this room."""
        hostiles = random.randint(1, 3)
        for xy in self.get_free_spaces(area, hostiles):
            monster_cls: Type[Character]
            monster_cls = Hostile
            monster_cls.spawn(area[xy], BasicHostile)
            self.entities += 1