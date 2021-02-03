from __future__ import annotations
from collections import defaultdict


class MapGrid(defaultdict):

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def size(self) -> int:
        return self._width * self._height

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        for i in range(self.size):
            self[i] = []
