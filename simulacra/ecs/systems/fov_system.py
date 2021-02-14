from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import tcod

from simulacra.core.options import *

from .system import System

if TYPE_CHECKING:
    from simulacra.core.game import Game


class FOVSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=[ 'IsPlayer' ])

        self._opaque = self.ecs.create_query(
            all_of=[ 'Opaque' ])

        self.transparent = np.ones(STAGE_SHAPE, dtype=np.bool, order="F")

    def update_fov(self) -> None:
        tile_grid = self.game.world.current_area.grid

        for opaque in self._opaque.result:
            x, y = opaque['Position'].xy
            self.transparent[x][y] = False

        tile_grid.visible = tcod.map.compute_fov(
            transparency=self.transparent,
            pov=self._query.result[0]['POSITION'].xy,
            radius=8,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
            )
        tile_grid.explored |= tile_grid.visible

    def update(self, dt):
        self.update_fov()
