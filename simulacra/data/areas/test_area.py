from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.options import *
from simulacra.world.area import Area

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class TestArea(Area):
    name = "TEST"

    def __init__(self, manager: AreaManager) -> None:
        super().__init__(manager)
        self.background = 0xFFFDCBB0

        for x in range(STAGE_WIDTH):
            for y in range(STAGE_HEIGHT):
                self.make_tile(x, y, 'decoration', 'grass_2')

        self.roll_asset(400, 80, 'decoration', ['grass_1'])
        self.roll_asset(400, 50, 'decoration', ['flowers_1', 'flowers_2'])
        self.roll_asset(200, 80, 'tree', ['tree_2'], transparent=False, passable=False)

        for x in range(0, 20):
            self.make_tile(x, 3, 'path', 'horizontal')
        self.make_tile(20, 3, 'path', 'turn_top_right')
        for y in range(4, 13):
            self.make_tile(20, y, 'path', 'vertical')
