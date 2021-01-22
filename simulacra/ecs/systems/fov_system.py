from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import tcod

from .system import System

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from simulacra.core.rendering.tile_grid import TileGrid


class FOVSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=['PLAYER']
            )

    def update_fov(self, tile_grid: TileGrid) -> None:
        tile_grid.visible = tcod.map.compute_fov(
            transparency=tile_grid.tiles["transparent"],
            pov=self._query.result[0]['POSITION'].ij,
            radius=10,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
            )
        tile_grid.explored |= tile_grid.visible

    def update(self, dt):
        self.update_fov(self._game.area.current_area.grid)
