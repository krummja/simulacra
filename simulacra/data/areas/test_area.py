from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.rendering.tile_grid import TileGrid
from simulacra.world.area import Area

if TYPE_CHECKING:
    from core.area_manager import AreaManager


class TestArea(Area):

    def __init__(self, manager: AreaManager) -> None:
        super().__init__(manager)

    def fill_area(self):
        tile = self._manager.game.ecs.engine.create_entity()
        tile.add('TILE', {
            'move_cost': 1,
            'transparent': True,
            'char': 57360,
            'color': (50, 50, 50),
            'bg': (0, 0, 0)
            })
        self.grid.tiles[:] = tile['TILE'].data

        wall = self._manager.game.ecs.engine.create_entity()
        wall.add('TILE', {
            'move_cost': 0,
            'transparent': False,
            'char': 57344,
            'color': (200, 100, 100),
            'bg': (0, 0, 0)
            })
        self.grid.tiles[10:20, 10] = wall['TILE'].data
        self.grid.tiles[22:32, 10] = wall['TILE'].data
