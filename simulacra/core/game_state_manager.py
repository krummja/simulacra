from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

from .manager import Manager
from .states.test_state import TestState

if TYPE_CHECKING:
    from .game import Game
    from .states.state import State


class GameStateManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._current_state = None
        self.states = {'TEST': TestState}
        self.transition('TEST')

    @property
    def current_state(self) -> State:
        return self._current_state

    def transition(self, state: str) -> None:
        self._current_state = self.states[state](self)

    def on_draw(self, **kwargs):
        self.current_state.on_draw(**kwargs)

    def handle_input(self):
        pass
