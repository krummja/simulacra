from __future__ import annotations
from typing import TYPE_CHECKING

import random

from simulacra.core.options import *
from simulacra.world.area import Area

if TYPE_CHECKING:
    from ecstremity import Entity
    from simulacra.core.area_manager import AreaManager


class TestArea(Area):
    name = "TEST"

    def __init__(self, manager: AreaManager) -> None:
        super().__init__(manager)

        for x in range(STAGE_WIDTH):
            for y in range(STAGE_HEIGHT):
                self.make_tile(x, y, 'decoration', 'grass_2')

        for _ in range(400):
            roll = random.randrange(0, 100)
            if roll <= 80:
                x = random.randrange(0, STAGE_WIDTH)
                y = random.randrange(0, STAGE_HEIGHT)
                self.make_tile(x, y, 'decoration', 'grass_1')

        for _ in range(400):
            roll = random.randrange(0, 100)
            if roll <= 50:
                x = random.randrange(0, STAGE_WIDTH)
                y = random.randrange(0, STAGE_HEIGHT)
                self.make_tile(x, y, 'decoration', 'flowers_1')
            roll = random.randrange(0, 100)
            if roll <= 50:
                x = random.randrange(0, STAGE_WIDTH)
                y = random.randrange(0, STAGE_HEIGHT)
                self.make_tile(x, y, 'decoration', 'flowers_2')

        for _ in range(200):
            roll = random.randrange(0, 100)
            if roll <= 80:
                x = random.randrange(0, STAGE_WIDTH)
                y = random.randrange(0, STAGE_HEIGHT)
                self.make_tile(x, y, 'tree', 'tree_2', transparent=False, passable=False)

        for x in range(0, 20):
            self.make_tile(x, 3, 'path', 'horizontal')
        self.make_tile(20, 3, 'path', 'turn_top_right')
        for y in range(4, 13):
            self.make_tile(20, y, 'path', 'vertical')
