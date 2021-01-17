from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulacra.core.game_state_manager import GameStateManager



class State:
    name: str

    def __init__(self, manager: GameStateManager) -> None:
        self.manager = manager
        self._commands = {}

    def on_draw(self) -> None:
        pass

    @property
    def commands(self):
        return self._commands
