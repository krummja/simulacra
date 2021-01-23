from __future__ import annotations
from typing import TYPE_CHECKING

from screeninfo import get_monitors
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
            width=(CONSOLE_WIDTH + 5) * TILE_SIZE,
            height=(CONSOLE_HEIGHT * TILE_SIZE),
            tileset=TILESET,
            title="Roguelike",
            renderer=tcod.RENDERER_SDL2,
            vsync=True
            )

        self._root_console = self._context.new_console(
            min_columns=(CONSOLE_WIDTH // 2) + 1,
            min_rows=(CONSOLE_HEIGHT // 2),
            magnification=MAGNIFICATION
            )

    @property
    def context(self) -> Context:
        return self._context

    @property
    def root_console(self) -> Console:
        return self._root_console

    def clear(self) -> None:
        self._root_console.clear()


def get_screen_dims():
    monitors = get_monitors()
    width = monitors[0].width
    height = monitors[0].height
    return width, height



