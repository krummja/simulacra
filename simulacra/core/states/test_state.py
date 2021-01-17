from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from .state import State
from ..input.input_controller import T

if TYPE_CHECKING:
    from simulacra.core.game_state_manager import GameStateManager


class TestState(State):
    name: str = "TEST"

    def cmd_confirm(self) -> Optional[T]:
        print("Command CONFIRM")
