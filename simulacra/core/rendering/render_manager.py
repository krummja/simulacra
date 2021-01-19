from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
from enum import Enum

from .character_map import TILESET
from ..manager import Manager

if TYPE_CHECKING:
    from ..game import Game
    from tcod.context import Context
    from tcod.console import Console


class TileSize(Enum):
    Small = 0
    Medium = 1
    Large = 2


class RenderManager(Manager):
    """Manager for handling the render console and running the render loop."""

    def __init__(self, game: Game) -> None:
        self._tilesize = [(110, 55), (90, 45), (80, 40)][TileSize.Medium.value]
        self._console_width = self._tilesize[0]
        self._console_height = self._tilesize[1]
        self._game = game
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

    def draw_ui(self) -> None:
        pass

    def render(self) -> None:
        pass
