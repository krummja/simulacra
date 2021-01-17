from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..input.input_controller import T
from .state import State

if TYPE_CHECKING:
    from simulacra.core.game_state_manager import GameStateManager


class TestState(State):
    name: str = "TEST"

    def cmd_confirm(self) -> Optional[T]:
        print("Command CONFIRM")
