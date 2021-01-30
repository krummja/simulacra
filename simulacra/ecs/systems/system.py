from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from ecstremity.query import Query


class System:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.ecs = self.game.ecs.engine
        self.query: Optional[Query] = None

    def update(self) -> None:
        pass
