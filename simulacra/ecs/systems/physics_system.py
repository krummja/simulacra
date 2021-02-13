from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from simulacra.core.options import *
from .system import System

from simulacra.utils.debug import *

if TYPE_CHECKING:
    from simulacra.core.game import Game


class PhysicsSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=['Blocker'])

        self.passable = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.bool, order="F")
        self.passable[:] = True

    def update(self, dt):
        for blocker in self._query.result:
            x, y = blocker['Position'].xy
            self.passable[x][y] = False
