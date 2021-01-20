from __future__ import annotations
from typing import TYPE_CHECKING

from .system import System

if TYPE_CHECKING:
    from simulacra.core.game import Game


class ActionSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=[
                'ACTOR'
                ]
            )
