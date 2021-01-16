from __future__ import annotations
from typing import TYPE_CHECKING

import random
import numpy as np
import tcod

from engine.geometry import Rect
from config import STAGE_WIDTH, STAGE_HEIGHT

if TYPE_CHECKING:
    from engine.areas.area import Area


class DungeonGenerator:

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            width: int = STAGE_WIDTH,
            height: int = STAGE_HEIGHT
        ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rooms = []
        self.map_data = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.int)

    def generate_rooms(self, max_rooms: int, min_size: int, max_size: int) -> None:
        for _ in range(max_rooms):
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            x = random.randint(self.x, self.x + self.width - w)
            y = random.randint(self.y, self.y + self.height - h)
            new_room = Rect.from_edges(left=x, top=y, right=w, bottom=h)
            if any(new_room.intersects(other) for other in self.rooms):
                continue

            # self.generate_connection(new_room, 80)

            self.map_data.T[new_room.inner] = 1
            self.rooms.append(new_room)

    def generate_connection(self, room: Rect, threshold: int) -> None:
        threshold = threshold if threshold <= 99 else 99
        if self.rooms:
            if random.randint(0, 99) < threshold:
                other_room = min(self.rooms, key=room.distance_to)
            else:
                other_room = self.rooms[-1]

            t_start = room.center
            t_end = other_room.center
            if random.randint(0, 1):
                t_middle = t_start[0], t_end[1]
            else:
                t_middle = t_end[0], t_start[1]

            self.map_data.T[tcod.line_where(*t_start, *t_middle)] = 2
            self.map_data.T[tcod.line_where(*t_middle, *t_end)] = 2
