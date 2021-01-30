from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from collections import deque

from simulacra.data.actions.action import Action, Impossible
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class PlayerManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
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
        player.add('Renderable', {'char': 0xE500, 'fg': 0xFFFF00FF, 'bg': None})
        player.add('Position', {'x': 1, 'y': 1})
        player.add('Player', {})
        player.add('Actor', {})
        player.add('Motility', {})
        player.add('Sprite', {})
        self._player_uid = player.uid
        return player

    def get_next_action(self):
        return self.action_queue.popleft()

    def move(self, direction: Tuple[int, int]) -> None:
        def blocked() -> bool:
            if self.game.area.current_area.is_blocked(
                self.position[0] + direction[0],
                self.position[1] + direction[1]
                ):
                return False
            return True
        action = Action(self.entity, 'try_move', direction, blocked).plan()
        self.action_queue.append(action.act)
