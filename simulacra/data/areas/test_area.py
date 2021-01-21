from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.rendering.tile_grid import TileGrid
from simulacra.world.area import Area

if TYPE_CHECKING:
    from core.area_manager import AreaManager


class TestArea(Area):

    def __init__(self, manager: AreaManager) -> None:
        super().__init__(manager)
