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
from engine.area import *
from engine.tile import *
from engine.graphic import *
from engine.tile_maps import *
from engine.hues import COLOR
from engine.model import Model
import engine.tile_maps

if TYPE_CHECKING:
    from engine.actor import Actor
    from engine.location import Location
    from engine.model import Model


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

    def place_entities(self, area: Area) -> None:
        """Spawn entities within this room."""
        npcs = random.randint(0, 3)
        items_spawned = random.randint(0, 2)
        for xy in self.get_free_spaces(area, npcs):
            monster_cls: Type[Character]
            monster_cls = NPC
            monster_cls.spawn(area[xy])


def generate(model: Model, width: int, height: int) -> Area:
    """Return a randomly generated Area."""

    room_max_size = 30
    room_min_size = 15
    max_rooms = 100

    area = Area(model, width, height)
    area.tiles[...] = WALL_01
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


BASE_MAP = np.array([
    "#######################",
    '#.....................#',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    'w.....................w',
    '#...C.............C...#',
    '#.....................#',
    '##ww##ww##   ##ww##ww##',
])

rules = [
    ('#', WALL_01),
    ('.', FLOOR),
    ('C', BARE_WALL_02),
    ('G', FLOOR_GRATE_01),
    ('c', CLUTTER_01),
    ('w', WINDOW_01)
]

def process_map(
        area: Area, 
        base: ndarray, 
        rules: List[Tuple[str, Tile]]
    ) -> ndarray:
    """Iterate through an 1D array consisting of char strings and replace
    for Tile instances based on a supplied list of rewrite rules."""
    height: int = base.shape[0]
    row: int = 0
    for line in base:
        width: int = len(line)
        col: int = 0
        if row <= height:
            for char in line:
                if col <= width:
                    for rule in rules:
                        if char == rule[0]:
                            area.tiles[row, col] = rule[1]
                    col += 1
            row += 1
    return area


# TODO: Oh now this is a neat idea - can I do rewrite rules based on broadcasting
# TODO: an entire array to a subset of a larger array?

array_rules = [
    (
        np.array(['###', '#.#', '###']),  # target template
        # some replacement
    )
]

map_test = process_map(Area(Model(), 50, 50), BASE_MAP, rules)

def test_area(model: Model) -> Area:
    area = Area(model, 110, 55)

    test_room = Room(0, 0, 20, 20)
    area.tiles[...] = FLOOR
    process_map(area, BASE_MAP, rules)

    area.player = Player.spawn(area[test_room.center], ai_cls=ai.PlayerControl)

    test_room.place_entities(area)

    area.update_fov()

    return area