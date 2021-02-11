from __future__ import annotations

import numpy as np
from simulacra.core.options import *
from simulacra.utils.map_grid import new_grid


class TileGrid:

    def __init__(self) -> None:
        self.shape = (STAGE_WIDTH, STAGE_HEIGHT)

        # Renderable Arrays
        self.saturated = np.zeros(self.shape, dtype=object, order="F")
        self.desaturated = np.zeros(self.shape, dtype=object, order="F")

        # Boolean Mask Arrays
        self.passable = np.ones(self.shape, dtype=np.bool, order="F")
        self.transparent = np.zeros(self.shape, dtype=np.bool, order="F")
        self.explored = np.zeros(self.shape, dtype=np.bool, order="F")
        self.visible = np.zeros(self.shape, dtype=np.bool, order="F")

    @property
    def width(self) -> int:
        return self.shape[0]

    @property
    def height(self) -> int:
        return self.shape[1]
