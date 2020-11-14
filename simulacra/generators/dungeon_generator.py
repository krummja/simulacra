from __future__ import annotations
from typing import TYPE_CHECKING

import random
from area import Area
from room import Room
from tiles.floors import *
from tiles.walls import *


class DungeonGenerator:

    max_rooms: int = 20
    max_room_size: int = 30
    min_room_size: int = 10
    rooms = []

    def generate(self, area: Area) -> Area:
        w = random.randint(self.min_room_size, self.max_room_size)
        h = random.randint(self.min_room_size, self.max_room_size)

        x = random.randint(0, area.width - w - 1)
        y = random.randint(0, area.height - h - 1)

        new_room = Room(x, y, w, h)

