from __future__ import annotations
from typing import TYPE_CHECKING

from .system import System

if TYPE_CHECKING:
    from simulacra.core.game import Game


class RenderSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self._game.ecs.engine.create_query(
            all_of=['RENDERABLE']
            )

    def render_visible_entities(self, area, console) -> None:
        pass

    def render(self) -> None:
        self._game.renderer.clear()
        for entity in self._query.result:
            self._game.renderer.root_console.print(2, 2, entity['RENDERABLE'].char)
