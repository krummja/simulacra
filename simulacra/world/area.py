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
        default_tile.add('TILE', {
            'char': self._sprites.get_codepoint('ground', 'grass_1'),
            'fg': 0xFFFFFFFF,
            'bg': 0xFF000000,
            'transparent': True,
            'move_cost': 1,
            'unformed': True
            })
        self._grid.ground[:] = default_tile

        test_tree = manager.game.ecs.engine.create_entity()
        test_tree.add('TILE', {
            'char': self._sprites.get_codepoint('tree', 'tree_2'),
            'fg': 0xFFFFFFFF,
            'bg': 0xFF000000,
            'transparent': True,
            'move_cost': 0,
            'unformed': True
            })

        for _ in range(100):
            roll = random.randrange(0, 100)
            if roll <= 50:
                x = random.randrange(0, self._grid.width)
                y = random.randrange(0, self._grid.height)
                self._grid.obstacle[x, y] = test_tree

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
        if self.grid.obstacle[x, y] != 0:
            if not self.grid.obstacle[x, y]['TILE'].move_cost:
                return True
        return False
