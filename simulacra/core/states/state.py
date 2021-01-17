from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulacra.core.game_state_manager import GameStateManager


class State:
    """All game states inherit from this class.

    A State is, fundamentally, a way of mapping input events to particular
    contexts which implement a view and a set of behaviors. I implement
    states as nodes of a finite state machine.

    Each state has an `on_draw` method for specific renderables on the
    render update. A state also has command methods, prefixed with
    `cmd_{name}`. Each command name must correspond to the name of a
    Command object in the command library.
    """
    name: str

    def __init__(self, manager: GameStateManager) -> None:
        self.manager = manager

    def on_draw(self) -> None:
        pass
