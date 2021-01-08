from __future__ import annotations
from typing import List

from engine.util import vector2
from engine.geometry.direction import Direction
from engine.geometry.rect import Rect
from engine.geometry.point import Point
from engine.geometry.size import Size


class Corridor:

    def __init__(
            self, *,
            start: Rect,
            direction: Direction,
            interval: int,
            count: int
        ) -> None:
        self._start = start
        self._points = [i * interval for i in range(count)]
        self._cells = []

        previous = start
        for _ in range(count):
            _direction = vector2(*direction.value)
            _hoffset = (((previous.width // 2) * _direction[0]) +
                        ((interval // 2) * _direction[0]))
            _voffset = (((previous.height // 2) * _direction[1]) +
                        ((interval // 2) * _direction[1]))
            _center = (int(previous.center.x + _hoffset), int(previous.center.y + _voffset))
            _new_cell = Rect.centered_at(
                center=Point(*_center),
                size=Size(interval, interval)
                )
            self._cells.append(_new_cell)
            previous = _new_cell

    @property
    def cells(self) -> List[Rect]:
        return self._cells

    @property
    def start(self) -> Rect:
        return min(self._cells)

    @property
    def end(self) -> Rect:
        return max(self._cells)
