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

        # TODO apparently walk this refactor back - performance nose dived :(

        default_tile = manager.game.ecs.engine.create_entity()
        # default_tile.add('POSITION', {})
        default_tile.add('RENDERABLE', {
            'char': self._sprites.get_codepoint('ground', 'grass_1'),
            })
        default_tile.add('TILE', {
            'transparent': True,
            'move_cost': 1,
            'unformed': True
            })
        self._grid.transparent[:] = default_tile['TILE'].transparent
        self._grid.ground[:] = default_tile

        for _ in range(100):
            roll = random.randrange(0, 100)
            if roll <= 50:
                x = random.randrange(0, self._grid.width)
                y = random.randrange(0, self._grid.height)
                test_tree = manager.game.ecs.engine.create_entity()
                test_tree.add('POSITION', {'x': x, 'y': y})
                test_tree.add('OBSTACLE', {})
                test_tree.add('RENDERABLE', {
                    'char': self._sprites.get_codepoint('tree', 'tree_2'),
                    })
                test_tree.add('TILE', {
                    'transparent': False,
                    'move_cost': 0,
                    'unformed': True
                    })
                self._grid.obstacle[x, y] = test_tree['RENDERABLE']
                self._grid.transparent[x, y] = test_tree['TILE'].transparent
                self._grid.move_cost[x, y] = test_tree['TILE'].move_cost

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
