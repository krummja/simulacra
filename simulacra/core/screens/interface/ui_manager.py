from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.manager import Manager

if TYPE_CHECKING:
    from tcod.console import Console
    from simulacra.core.game import Game


class UIManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def update(self, dt) -> None:
        pass
