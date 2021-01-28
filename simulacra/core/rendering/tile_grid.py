from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from .tile_data import tile_graphic, tile_dt
from simulacra.core.options import *

if TYPE_CHECKING:
    from .render_manager import RenderManager


class TileGrid:

    def __init__(self) -> None:
        self.shape = (STAGE_WIDTH, STAGE_HEIGHT)
        self.tiles = np.zeros(self.shape, dtype=object)
        self.explored = np.zeros(self.shape, dtype=np.bool)
        self.visible = np.zeros(self.shape, dtype=np.bool)

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def height(self) -> int:
        return self.shape[0]
