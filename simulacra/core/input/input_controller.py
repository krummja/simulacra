from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, Optional, TypeVar

import tcod
from tcod.event import EventDispatch

from ..manager import Manager
from .commands import CommandLibrary

if TYPE_CHECKING:
    from ..game import Game

T = TypeVar("T")


class InputController(Generic[T], EventDispatch[T], Manager):
    """Inherits TCOD's EventDispatch to provide basic input mapping.
    Commands are handled separately in the CommandManager.
    """

    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._current_state = game.state.current_state

    def handle_input(self) -> Callable[[], Optional[T]]:
        for event in tcod.event.get():
            value: Callable[[], Optional[T]] = self.dispatch(event)
            if value is not None:
                return value

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in CommandLibrary.COMMAND_KEYS:
            func = getattr(self._current_state,
                           f"cmd_{CommandLibrary.COMMAND_KEYS[event.sym]}")
            return func()
        if event.sym in CommandLibrary.MOVE_KEYS:
            return self._current_state.cmd_move(*CommandLibrary.MOVE_KEYS[event.sym])
        return None
