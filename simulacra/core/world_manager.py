from __future__ import annotations
from typing import TYPE_CHECKING

from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class WorldManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
