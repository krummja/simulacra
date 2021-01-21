from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.rendering.tile_grid import TileGrid

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class Area:

    def __init__(self, manager: AreaManager) -> None:
        self._manager = manager
        self._tiles = TileGrid(self._manager._game.renderer)

    @property
    def tiles(self) -> TileGrid:
        return self._tiles

    @property
    def width(self) -> int:
        return self._tiles.width

    @property
    def height(self) -> int:
        return self._tiles.height
