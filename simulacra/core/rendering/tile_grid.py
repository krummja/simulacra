from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from simulacra.core.options import *

if TYPE_CHECKING:
    from .render_manager import RenderManager


class TileGrid:

    def __init__(self) -> None:
        self.shape = (STAGE_WIDTH, STAGE_HEIGHT)
        self.tiles = np.zeros(self.shape, dtype=object, order="F")
        self.explored = np.zeros(self.shape, dtype=np.bool, order="F")
        self.visible = np.zeros(self.shape, dtype=np.bool, order="F")

    @property
    def width(self) -> int:
        return self.shape[0]

    @property
    def height(self) -> int:
        return self.shape[1]
