from __future__ import annotations
from typing import TYPE_CHECKING

from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class PlayerManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._player_uid = None
        self.initialize_player()

    @property
    def entity(self):
        return self._game.ecs.engine.get_entity(self._player_uid)

    @property
    def uid(self):
        return self._player_uid

    def initialize_player(self):
        player = self._game.ecs.engine.create_entity()
        player.add('Renderable', {'char': '@', 'color': '#f0f', 'bg': '#000'})
        print(vars(player))
        return player
