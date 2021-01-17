from __future__ import annotations
from typing import TYPE_CHECKING

import tcod

from .manager import Manager
from .rendering.character_map import CharacterMap

if TYPE_CHECKING:
    from .game import Game
    from tcod.context import Context
    from tcod.console import Console


TILESET = tcod.tileset.load_tilesheet(
    path="./simulacra/assets/simulacra16x16.png",
    columns=16,
    rows=48,
    charmap=CharacterMap().data
    )


class ConsoleManager(Manager):

    def __init__(self, game: Game) -> None:
        self._console_width = 110
        self._console_height = 55
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
