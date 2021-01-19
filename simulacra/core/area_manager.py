from __future__ import annotations
from typing import TYPE_CHECKING

from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class AreaManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._current_area = None

    @property
    def current_area(self):
        return self._current_area
