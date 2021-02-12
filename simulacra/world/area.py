from __future__ import annotations
from typing import Tuple, List, TYPE_CHECKING

import random

from simulacra.core.options import *
from simulacra.utils.geometry import Rect, Point
from simulacra.core.rendering.tile_grid import TileGrid

if TYPE_CHECKING:
    from simulacra.core.world_manager import WorldManager
    from simulacra.core.area_manager import AreaManager


class Area:

    name: str = ""

    def __init__(self, world: WorldManager) -> None:
        self._world = world
        self._grid = TileGrid()

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
        if not self.grid.passable[x, y]:
            return True
        return False
