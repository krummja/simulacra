from __future__ import annotations
from typing import List, TYPE_CHECKING

import random
import numpy as np

from engine.util import vector2
from engine.geometry.direction import Direction
from engine.geometry.rect import Rect
from engine.geometry.point import Point
from engine.geometry.size import Size


class Rooms:

    def __init__(self, *, start: Point, direction: Direction) -> None:
        self._start = start
        self._direction = direction.value
        self._rooms = []
        self._connections = []

    def _generate_rooms(self):
        pass
