from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
from enum import Enum

from .rendering.character_map import TILESET
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game
    from tcod.context import Context
    from tcod.console import Console


class ConsoleManager(Manager):
    """Manager for handling in-game log messages."""

    def __init__(self, game: Game) -> None:
        self.game = game
