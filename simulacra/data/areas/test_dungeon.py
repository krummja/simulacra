from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.options import *
from simulacra.world.area import Area

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class TestDungeon(Area):
    name = "DUNGEON"

    def __init__(self, manager: AreaManager) -> None:
        super().__init__(manager)
        self.background = 0xFF3E3546

        for x in range(STAGE_WIDTH):
            for y in range(STAGE_HEIGHT):
                self.make_tile(x, y, 'dungeon', 'wall/void', passable=False, transparent=False)

        for x in range(2, 12):
            for y in range(2, 12):
                self.make_tile(x, y, 'dungeon', 'floor/stone_1')
