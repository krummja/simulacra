from __future__ import annotations
from typing import TYPE_CHECKING

import random

from simulacra.core.options import *
from simulacra.core.rendering.tile_grid import TileGrid

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class Area:

    name: str = ""

    def __init__(self, manager: AreaManager) -> None:
        self._manager = manager
        self._tiles = TileGrid()

        default_tile = manager.game.ecs.engine.create_entity()
        default_tile.add('TILE', {
            'char': 0xE000+16+16+16,
            'fg': 0xAAAAAAAA,
            'bg': 0xFF000000,
            'transparent': True,
            'move_cost': 1,
            'unformed': True
            })
        self._tiles.tiles[:] = default_tile

    @property
    def grid(self) -> TileGrid:
        return self._tiles

    @property
    def width(self) -> int:
        return self._tiles.width

    @property
    def height(self) -> int:
        return self._tiles.height

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.grid.tiles[x, y]['TILE'].move_cost:
            return True
        return False
