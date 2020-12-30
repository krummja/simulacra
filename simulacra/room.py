from __future__ import annotations

import random
from typing import Iterator

from area import *
from geometry.rect import Rect
from geometry.span import Span
from graphic import *


class Room:

    def __init__(
            self: Room,
            x: int,
            y: int,
            width: int,
            height: int,
            max_entities: int=3,
            room_id: str = ""
        ) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.entities = 0
        self.max_entities = max_entities
        self.room_id = room_id

    @property
    def outer(self) -> Tuple[slice, slice]:
        """Return the NumPy index for the whole room."""
        index: Tuple[slice, slice] = np.s_[self.x1: self.x2, self.y1: self.y2]
        return index

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the NumPy index for the inner room area."""
        index: Tuple[slice, slice] = np.s_[
            self.x1 + 1: self.x2 - 1, self.y1 + 1: self.y2 - 1
            ]
        return index

    @property
    def bounds(self):
        return Rect.from_spans(
            vertical=Span(self.x1, self.y1+self.height),
            horizontal=Span(self.y1, self.x1+self.width)
            )

    @property
    def center(self) -> Tuple[int, int]:
        """Return the index for the room's center coordinate."""
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    @property
    def x(self) -> int:
        return self.center[0]

    @property
    def y(self) -> int:
        return self.center[1]

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
