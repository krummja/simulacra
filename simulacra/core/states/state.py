from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from ..input import T, StateBreak

if TYPE_CHECKING:
    from tcod.console import Console
    from simulacra.core.game_state_manager import GameStateManager


class State:
    """All game states inherit from this class.

    A State is, fundamentally, a way of mapping input events to particular
    contexts which implement a view and a set of behaviors. I implement
    states as nodes of a finite state machine.

    Each state has an `on_draw` method for specific renderables on the
    render update. A state also has command methods, prefixed with
    `cmd_{name}`. Each command name must correspond to a registered
    input -> command mapping in the CommandLibrary.
    """
    name: str

    def __init__(self, manager: GameStateManager) -> None:
        self.manager = manager
        self._view = None

    def on_draw(self, console: Console) -> None:
        self._view.on_draw(console)

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self) -> Optional[T]:
        raise StateBreak()

    def cmd_examine(self) -> Optional[T]:
        pass

    def cmd_equipment(self) -> Optional[T]:
        pass

    def cmd_inventory(self) -> Optional[T]:
        print("Inventory")

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_pickup(self) -> Optional[T]:
        pass

    def cmd_quit(self) -> Optional[T]:
        raise SystemExit()
