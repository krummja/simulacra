from __future__ import annotations
from typing import TYPE_CHECKING

from collections import defaultdict
from simulacra.core.options import *
from simulacra.utils.geometry.array2d import Array2D
from simulacra.core.rendering.tile_grid import TileGrid

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class Tile(defaultdict):
    def __init__(
            self,
            char: str = chr(0xE003),
            fg: str = "dark green",
            bg: str = None,
            transparent: bool= True,
            move_cost: int = 1,
            unformed: bool= True
        ) -> None:
        self["char"] = char
        self["fg"] = fg
        self["bg"] = bg
        self["transparent"] = transparent
        self["move_cost"] = move_cost
        self["unformed"] = unformed


class Area:

    name: str = ""

    def __init__(self, manager: AreaManager) -> None:
        self._manager = manager
        base_tile = self._manager.game.ecs.engine.create_entity()
        base_tile.add('TILE', Tile())
        self._tiles = Array2D(
            STAGE_WIDTH,
            STAGE_HEIGHT,
            base_tile
            )

        test_tile = self._manager.game.ecs.engine.create_entity()
        test_tile.add('TILE', Tile(fg="red"))
        for i in range(STAGE_HEIGHT):
            self._tiles[20, i] = test_tile

    @property
    def grid(self) -> TileGrid:
        return self._tiles

    @property
    def width(self) -> int:
        return self._tiles.width

    @property
    def height(self) -> int:
        return self._tiles.height

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.grid[x, y]['TILE'].move_cost:
            return True
        return False
