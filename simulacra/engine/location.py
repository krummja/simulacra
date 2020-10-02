from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.area import Area


class Location:

    area: Area

    x: int
    y: int

    @property
    def xy(self: Location) -> Tuple[int, int]:
        return self.x, self.y

    @xy.setter
    def xy(self: Location, xy: Tuple[int, int]) -> None:
        self.x, self.y = xy

    @property
    def ij(self: Location) -> Tuple[int, int]:
        return self.y, self.x

    def distance_to(self: Location, x: int, y: int) -> int:
        return max(abs(self.x - x), abs(self.y - y))

    def relative(self: Location, x: int, y: int) -> Tuple[int, int]:
        return self.x + x, self.y + y
