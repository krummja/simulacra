from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from core.game import Game


class Manager(ABC):

    @property
    def game(self) -> Game:
        return self._game

    @game.setter
    def game(self, value: Game) -> None:
        self._game = value
