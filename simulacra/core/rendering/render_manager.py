from __future__ import annotations
from typing import TYPE_CHECKING

from ..manager import Manager

if TYPE_CHECKING:
    from ..game import Game


class RenderManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._root_console = game.console.root_console

    def render(self) -> None:
        self._root_console.clear()
        self._game.interface.current_view.on_draw(self._root_console)
