from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from .state import State, T, StateBreak

if TYPE_CHECKING:
    from simulacra.core.states.game_state_manager import GameStateManager


class PlayerReady(State):
    name: str = "PLAYER_READY"

    def __init__(self, manager: GameStateManager) -> None:
        super().__init__(manager)

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def on_update(self):
        pass

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self) -> Optional[T]:
        raise StateBreak()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_drop(self) -> Optional[T]:
        pass

    def cmd_equipment(self) -> Optional[T]:
        pass

    def cmd_examine(self) -> Optional[T]:
        pass

    def cmd_inventory(self) -> Optional[T]:
        pass

    def cmd_pickup(self) -> Optional[T]:
        pass

    def cmd_quit(self) -> Optional[T]:
        raise SystemExit()