from __future__ import annotations
from typing import Generator, List, Optional

from enum import Enum
import random
import tcod
import numpy as np

from content.areas.generators.algorithm import Algorithm
from engine.geometry.rect import Rect


class RoomBuilder(Algorithm):

    def __init__(
            self, *,
            max_rooms: int,
            min_size: int,
            max_size: int,
        ) -> None:
        super().__init__()
        self.max_rooms = max_rooms
        self.min_size = min_size
        self.max_size = max_size
        self.working = np.zeros((256, 256), dtype=np.int)

    def execute(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
        ) -> Generator[Rect, None, None]:

        _rooms = []
        for _ in range(self.max_rooms):
            _w = random.randint(self.min_size, self.max_size)
            _h = random.randint(self.min_size, self.max_size)
            _x = random.randint(x, x + width - _w - 1)
            _y = random.randint(y, y + height - _h - 1)

            _new: Rect = Rect.from_edges(left=_x, top=_y, right=_x+_w, bottom=_y+_h)
            if any(_new.intersects(other) for other in _rooms):
                continue
            _rooms.append(_new)
            yield _new
