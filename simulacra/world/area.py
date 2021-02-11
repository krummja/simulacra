from __future__ import annotations
from typing import List, TYPE_CHECKING

import random

from simulacra.core.options import *
from simulacra.core.rendering.tile_grid import TileGrid

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class Area:

    name: str = ""

    def __init__(self, manager: AreaManager) -> None:
        self._manager = manager
        self._grid = TileGrid()
        self._sprites = self._manager.game.renderer.sprites

    @property
    def grid(self) -> TileGrid:
        return self._grid

    @property
    def width(self) -> int:
        return self._grid.width

    @property
    def height(self) -> int:
        return self._grid.height

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 1 <= y < self.height):
            return True
        if not self.grid.passable[x, y]:
            return True
        return False

    # TODO: Move this to the Architect
    def make_tile(
            self,
            x: int,
            y: int,
            registry: str,
            name: str,
            transparent: bool = True,
            passable: bool = True,
        ) -> None:
        tile = self._manager.game.ecs.engine.create_entity()
        tile.add('Renderable', {
            'codepoint': self._sprites.get_codepoint(registry, name, saturated=True),
            'variant': self._sprites.get_codepoint(registry, name, saturated=False)
            })
        tile.add('Tile', {
            'transparent': transparent,
            'passable': passable,
            'unformed': True,
            })
        self._grid.saturated[x, y] = tile['Renderable'].char
        self._grid.desaturated[x, y] = tile['Renderable'].variant
        self._grid.transparent[x, y] = tile['Tile'].transparent
        self._grid.passable[x, y] = tile['Tile'].passable

    # TODO: Move this to the Architect.
    def roll_asset(
            self,
            iterations: int,
            threshold: int,
            registry: str,
            names: List[str],
            transparent: bool = True,
            passable: bool = True,
        ) -> None:
        for _ in range(iterations):
            for name in names:
                roll = random.randrange(0, 100)
                if roll <= threshold:
                    x = random.randrange(0, STAGE_WIDTH)
                    y = random.randrange(0, STAGE_HEIGHT)
                    self.make_tile(
                        x, y,
                        registry,
                        name,
                        transparent=transparent,
                        passable=passable
                        )
