from __future__ import annotations
from typing import Callable, Tuple, TYPE_CHECKING, NamedTuple
from collections import deque

from simulacra.geometry.direction import Direction
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game
    from ecstremity import EntityEvent


class PlayerManager(Manager):

    def __init__(self, game: Game) -> None:
        self.game = game
        self.action_queue = deque([])

        self._player_uid = None
        self.initialize_player()

    @property
    def entity(self):
        return self.game.ecs.engine.get_entity(self._player_uid)

    @property
    def uid(self):
        return self._player_uid

    @property
    def is_turn(self) -> bool:
        return self.entity['ACTOR'].has_energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.entity['POSITION'].xy

    def initialize_player(self):
        player = self.game.ecs.engine.create_entity()
        player.add('Renderable', {'char': '@', 'color': '#f0f', 'bg': '#000'})
        player.add('Position', {'x': 10, 'y': 10})
        player.add('Player', {})
        player.add('Actor', {})
        self._player_uid = player.uid
        return player

    def get_next_action(self):
        return self.action_queue.popleft()

    def move(self, direction: Tuple[int, int]) -> None:
        def act():
            self.entity.fire_event('try_move', direction)
        self.action_queue.append(act)
