from __future__ import annotations
from typing import Tuple

import numpy as np


class Room:

    def __init__(
            self: Room,
            x: int,
            y: int,
            width: int,
            height: int,
        ) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

    @property
    def outer(self) -> Tuple[slice, slice]:
        """Return the NumPy index for the whole room."""
        index: Tuple[slice, slice] = np.s_[self.x1:self.x2, self.y1:self.y2]
        return index

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the NumPy index for the inner room area."""
        index: Tuple[slice, slice] = np.s_[
            self.x1 + 1:self.x2 - 1, self.y1 + 1:self.y2 - 1
            ]
        return index

    @property
    def center(self) -> Tuple[int, int]:
        """Return the index for the room's center coordinate."""
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    @property
    def area(self):
        return (self.width * self.height)

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


a = Room(0, 0, 10, 10)
b = Room(3, 3, 10, 10)

print(a.center)
print(b.center)

print(a.intersects(b))

SI = max(0, min(a.x2, b.x2) - max(a.x1, b.x1)) * max(0, min(a.y2, b.y2) - max(a.y1, b.y1))
print(SI)

