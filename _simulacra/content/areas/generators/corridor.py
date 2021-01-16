from __future__ import annotations
from typing import Generator, List, Optional

from enum import Enum
import random
import tcod
import numpy as np

from content.areas.generators.algorithm import Algorithm
from engine.util import vector2
from engine.geometry.direction import Direction
from engine.geometry.rect import Rect
from engine.geometry.point import Point
from engine.geometry.size import Size


class Corridor(Algorithm):

    def __init__(
            self, *,
            start: Rect,
            end: Rect,
            size: int
        ) -> None:
        super().__init__()
        _distance = start.distance_to(end)
        _count = _distance // size

        if start.center.x < end.center.x:
            _h_direction = Direction.right
        else:
            _h_direction = Direction.left

        if start.center.y < end.center.y:
            _v_direction = Direction.down
        else:
            _v_direction = Direction.up

        previous = start
        for _ in range(_count):
            pass

    def execute(self) -> Generator[Rect, None, None]:
        pass
