from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from .tile_data import tile_graphic, tile_dt
from simulacra.core.game import Options

if TYPE_CHECKING:
    from .render_manager import RenderManager


class TileGrid:

    def __init__(self, manager: RenderManager) -> None:
        self.manager = manager
        self.shape = (Options.STAGE_HEIGHT, Options.STAGE_WIDTH)
        self.tiles = np.zeros(self.shape, dtype=tile_dt)
        self.effects = np.zeros(self.shape, dtype=tile_graphic)
        self.explored = np.zeros(self.shape, dtype=np.bool)
        self.visible = np.zeros(self.shape, dtype=np.bool)
