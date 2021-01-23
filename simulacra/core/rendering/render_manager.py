from __future__ import annotations
from typing import TYPE_CHECKING

import tcod

from simulacra.core.options import *
from .character_map import TILESET
from ..manager import Manager

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.context import Context
    from ..game import Game


class RenderManager(Manager):
    """Manager for handling the render console."""

    def __init__(self, game: Game) -> None:
        self.game = game

        self._context = tcod.context.new_window(
            width=CONSOLE_WIDTH * TILE_SIZE,
            height=CONSOLE_HEIGHT * TILE_SIZE,
            tileset=TILESET,
            title="Roguelike",
            renderer=tcod.RENDERER_SDL2,
            vsync=True
            )

        self._root_console = tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT)

    @property
    def context(self) -> Context:
        return self._context

    @property
    def root_console(self) -> Console:
        return self._root_console

    def clear(self) -> None:
        self._root_console.clear()
