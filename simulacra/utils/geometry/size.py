"""ENGINE.GEOMETRY.Size"""
from __future__ import annotations

from typing import Type


class Size(tuple):
    """Base class for defining a 2D area.

    Supports floor division.
    """

    def __new__(cls: Type[Size], width: int, height: float) -> Size:
        assert width >= 0
        assert height >= 0
        return super().__new__(cls, (width, height))

    def __floordiv__(self, n) -> Size:
        if not isinstance(n, (int, float)):
            return NotImplemented
        assert n > 0
        return Size(self[0] // n, self[1] // n)

    @property
    def width(self) -> int:
        return self[0]

    @property
    def height(self) -> float:
        return self[1]

    @property
    def area(self) -> float:
        return self.width * self.height
