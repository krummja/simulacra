from __future__ import annotations
from typing import (Callable, Generic, Optional, TypeVar, TYPE_CHECKING)

import tcod
from tcod.event import EventDispatch

from ..manager import Manager

if TYPE_CHECKING:
    from ..states.state import State
    from ..game import Game
    from .commands import Command

T = TypeVar("T")


class InputController(Generic[T], EventDispatch[T], Manager):
    """Inherits TCOD's EventDispatch to provide basic input mapping.

    Commands are handled separately in the CommandManager.
    """

    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._current_state = self._game.state.current_state

    @property
    def current_state(self) -> State:
        return self._current_state

    def handle_input(self) -> Callable[[], Optional[T]]:
        for event in tcod.event.get():
            value: Callable[[], Optional[T]] = self.dispatch(event)
            if value is not None:
                return value

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if self._current_state is not None:
            command: Command = self.game.commands.on_input_event(event)
            if command:
                getattr(self._current_state, f"cmd_{command.name}")
                command()
            return None
