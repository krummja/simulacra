from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.options import *
from simulacra.world.grid import TileGrid


if TYPE_CHECKING:
    from simulacra.core.world_manager import WorldManager


class Area:

    def __init__(self, manager: WorldManager) -> None:
        self._manager = manager
        self._grid = TileGrid(self, STAGE_WIDTH, STAGE_HEIGHT)

    def initialize_area(self):
        self._grid.initialize_tiles()
        self._grid.fill_tiles()

    @property
    def grid(self) -> TileGrid:
        return self._grid

    @property
    def width(self) -> int:
        return self._grid.width

    @property
    def height(self) -> int:
        return self._grid.height

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 1 <= y < self.height):
            return True
        if not self.grid.tiles[x][y].passable:
            return True
        return False
