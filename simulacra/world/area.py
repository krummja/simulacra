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
        self._grid = TileGrid()
        self._sprites = self._manager.game.renderer.sprites

        default_tile = manager.game.ecs.engine.create_entity()
        default_tile.add('RENDERABLE', {
            'char': self._sprites.get_codepoint('ground', 'tile_1'),
            })
        default_tile.add('TILE', {
            'transparent': True,
            'move_cost': 1,
            'unformed': True
            })
        self._grid.transparent[:] = default_tile['TILE'].transparent
        self._grid.ground[:] = default_tile

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
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if self.grid.move_cost[x, y] != 0:
            if not self.grid.move_cost[x, y]:
                return True
        if self.grid.move_cost[x, y] == 0:
            return True
        return False
