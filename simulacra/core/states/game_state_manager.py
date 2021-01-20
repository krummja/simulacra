from __future__ import annotations
from typing import Dict, Type, TYPE_CHECKING

from ..manager import Manager
from .test_state import TestState

if TYPE_CHECKING:
    from ..game import Game
    from .state import State


class GameStateManager(Manager):

    def __init__(self, game: Game) -> None:
        self.game = game
        self._current_state = None
        self.states: Dict[str, Type[State]] = {
            'TEST': TestState
            }
        self.transition('TEST')

    @property
    def current_state(self) -> State:
        return self._current_state

    def transition(self, state: str) -> None:
        self._current_state = self.states[state](self)
