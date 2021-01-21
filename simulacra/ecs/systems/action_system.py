from __future__ import annotations
from typing import TYPE_CHECKING
from collections import deque

from .system import System

from simulacra.utils.debug import *

if TYPE_CHECKING:
    from simulacra.core.game import Game


class ActionSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=['ACTOR'])

    def update(self, dt):
        entities = self._query.result
        entities = sorted(entities, key=lambda e: e['ACTOR'])
        entities = deque(entities)

        entity = entities[0]

        if entity and not entity['ACTOR'].has_energy:
            self.game.clock.increment(-1 * entity['ACTOR'].energy)
            for e in entities:
                e['ACTOR'].add_energy(self.game.clock.tick_delta)

        while entity and entity['ACTOR'].has_energy:

            # TODO Add logic for incapacitation, etc.

            if entity.has('PLAYER'):
                try:
                    # NOTE No actions available, thus no rendering
                    action = self.game.player.get_next_action()
                    if action:
                        action()
                    return True
                except IndexError:
                    return False

            entity.fire_event('take-action')
            entity = entities.popleft()

        return False
