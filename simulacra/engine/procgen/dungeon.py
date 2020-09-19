from __future__ import annotations  # type: ignore
from typing import Iterator, List, Tuple, Type, TYPE_CHECKING

import random

import numpy as np
import tcod

from engine.actions import ai, Action
from engine.paths import Fighter
from engine.paths.player import Player
from engine.area import *
from engine.tile import *
from engine.graphic import *
import engine.tile_maps

if TYPE_CHECKING:
    from engine.actor import Actor
    from engine.location import Location
    from engine.model import Model


WALL = Tile(
    move_cost=0,
    transparent=False,
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
    dark=(ord(" "), (255, 255, 255), (0, 0, 100))
)

FLOOR = Tile(
    move_cost=1,
    transparent=True,
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
    dark=(ord(" "), (255, 255, 255), (50, 50, 150))
)


class Room:

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

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

    def get_free_spaces(self, area: Area, number: int) -> Iterator[Tuple[int, int]]:
        """Iterate over the x,y coordinates up to `number` spaces."""
        for _ in range(number):
            x = random.randint(self.x1 + 1, self.x2 - 2)
            y = random.randint(self.y1 + 1, self.y2 - 2)
            if area.is_blocked(x, y):
                continue
            yield x, y

    def place_entities(self, area: Area) -> None:
        """Spawn entities within this room."""
        pass


def generate(model: Model, width: int, height: int) -> Area:
    """Return a randomly generated Area."""

    room_max_size = 30
    room_min_size = 15
    max_rooms = 100

    area = Area(model, width, height)
    area.tiles[...] = WALL
    rooms: List[Room] = []

    for i in range(max_rooms):
        w = random.randint(room_min_size, room_max_size)
        h = random.randint(room_min_size, room_max_size)

        x = random.randint(0, width - w)
        y = random.randint(0, height - h)

        new_room = Room(x, y, w, h)
        if any(new_room.intersects(other) for other in rooms):
            continue

        area.tiles.T[new_room.inner] = FLOOR

        if rooms:
            if random.randint(0, 99) < 80:
                other_room = min(rooms, key=new_room.distance_to)
            else:
                other_room = rooms[-1]
            
            t_start = new_room.center
            t_end = other_room.center

            if random.randint(0, 1):
                t_middle = t_start[0], t_end[1]
            else:
                t_middle = t_end[0], t_start[1]
            
            area.tiles.T[tcod.line_where(*t_start, *t_middle)] = FLOOR
            area.tiles.T[tcod.line_where(*t_middle, *t_end)] = FLOOR
        rooms.append(new_room)

    area.player = Player.spawn(area[rooms[0].center], ai_cls=ai.PlayerControl)

    area.update_fov()
    return area