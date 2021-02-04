from __future__ import annotations

import numpy as np
from simulacra.core.options import *


class TileGrid:

    def __init__(self) -> None:
        self.shape = (STAGE_WIDTH, STAGE_HEIGHT)

        # Tile Arrays
        self.ground = np.zeros(self.shape, dtype=object, order="F")
        self.obstacle = np.zeros(self.shape, dtype=object, order="F")

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
