from __future__ import annotations
from typing import Tuple

from ecstremity import Component


class Position(Component):
    name = "POSITION"

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y

    @xy.setter
    def xy(self, value: Tuple[int, int]) -> None:
        self.x = value[0]
        self.y = value[1]

    @property
    def ij(self) -> Tuple[int, int]:
        return self.y, self.x
