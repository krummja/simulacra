from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from ..input import T, StateBreak

if TYPE_CHECKING:
    from simulacra.core.states.game_state_manager import GameStateManager


class State:
    """All game states inherit from this class.

    States are essentially domains that restrict input events to certain
    well-defined contexts.
    """
    name: str

    def __init__(self, manager: GameStateManager) -> None:
        self.manager = manager

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def on_update(self):
        pass

    def cmd_confirm(self) -> Optional[T]:
        """
        [ENTER]
        Context: DEFAULT
        """

    def cmd_escape(self) -> Optional[T]:
        """
        [ESCAPE]
        Context: DEFAULT
        """
        raise StateBreak()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        """
        Arrow Keys, Keypad
        Context: DEFAULT
        """

    def cmd_drop(self) -> Optional[T]:
        """
        Default: [D]
        Context: STAGE
        """

    def cmd_equipment(self) -> Optional[T]:
        """
        Default: [E]
        Context: STAGE
        """

    def cmd_examine(self) -> Optional[T]:
        """
        Default: [L]
        Context: STAGE
        """

    def cmd_inventory(self) -> Optional[T]:
        """
        Default: [I]
        Context: STAGE
        """

    def cmd_pickup(self) -> Optional[T]:
        """
        Default: [G]
        Context: STAGE
        """

    def cmd_quit(self) -> Optional[T]:
        """
        Default: [Q],
        Context: MAIN_MENU
        """
        raise SystemExit()
