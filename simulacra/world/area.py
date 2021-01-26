from __future__ import annotations
from typing import TYPE_CHECKING

from collections import defaultdict
from simulacra.core.options import *
from simulacra.utils.geometry.array2d import Array2D

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class Tile(defaultdict):
    def __init__(
            self,
            char: str = chr(0xE006),
            fg: str = 0xFF888888,
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
            STAGE_WIDTH - 3,
            STAGE_HEIGHT - 1,
            base_tile
            )

    @property
    def grid(self) -> Array2D:
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