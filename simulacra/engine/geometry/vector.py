from __future__ import annotations
from typing import Final, TYPE_CHECKING, Type

import math

if TYPE_CHECKING:
    pass


class Vec(tuple):

    def __new__(cls: Type[Vec], x: int, y: int) -> Vec:
        return tuple.__new__(cls, (x, y))

    @property
    def area(self) -> float:
        return self[0] * self[1]


