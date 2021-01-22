from __future__ import annotations
from typing import List, TYPE_CHECKING

import numpy as np
import tcod

from .tile_data import tile_graphic
from .character_map import TILESET
from ..manager import Manager

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.context import Context
    from ..game import Game
    from .tile_grid import TileGrid


class RenderManager(Manager):
    """Manager for handling the render console."""

    def __init__(self, game: Game) -> None:
        self.game = game
        self._tilesize = [(110, 55), (90, 45), (80, 40)][1]
        self._console_width = self._tilesize[0]
        self._console_height = self._tilesize[1]
        self._console_config = {
            'columns': self._console_width,
            'rows': self._console_height,
            'tileset': TILESET,
            'title': "Simulacra",
            'vsync': True,
            }
        self._context: Context = tcod.context.new_terminal(**self._console_config)
        self._root_console: Console = tcod.Console(self._console_width,
                                                   self._console_height)

    @property
    def context(self) -> Context:
        return self._context

    @property
    def root_console(self) -> Console:
        return self._root_console

    def clear(self) -> None:
        self._root_console.clear()

    # noinspection PyTypeChecker
    def select_tile_mask(self, tile_grid: TileGrid, world_view) -> np.ndarray:
        UNKNOWN = np.asarray((0, (0, 0, 0), (0, 0, 0)), dtype=tile_graphic)

        if_visible = tile_grid.visible[world_view]
        if_explored = tile_grid.explored[world_view]
        lit_tiles = tile_grid.tiles["light"][world_view]
        unlit_tiles = tile_grid.tiles["dark"][world_view]

        condlist = (if_visible, if_explored)
        choicelist = (lit_tiles, unlit_tiles)
        return np.select(condlist=condlist,
                         choicelist=choicelist,
                         default=UNKNOWN)
