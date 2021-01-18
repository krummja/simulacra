from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, Optional, TypeVar

import tcod
from tcod.event import EventDispatch

from ..manager import Manager

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
        self._game.commands.on_input_event(event)
        try:
            command = self._game.commands.get_next_command()
            func = getattr(self._current_state,
                           f"cmd_{command.name}")
            return func()
        except AttributeError:
            return None
