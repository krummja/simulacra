from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, Optional, TypeVar

import tcod
from tcod.event import EventDispatch

from ..manager import Manager
from .commands import CommandLibrary

if TYPE_CHECKING:
    from ..game import Game

T = TypeVar("T")


class StateBreak(Exception):
    """Break current state and force it to return None."""


class InputController(Generic[T], EventDispatch[T], Manager):
    """Inherits TCOD's EventDispatch to provide basic input mapping.
    Commands are handled separately in the CommandManager.
    """

    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._current_state = game.state.current_state

    def handle_input(self) -> Callable[[], Optional[T]]:
        all_key_events = list(tcod.event.get())
        key_events = [e for e in all_key_events if e.type == 'KEYDOWN']
        if len(key_events) > 0:
            event = key_events.pop()
            try:
                value: Callable[[], Optional[T]] = self.dispatch(event)
            except StateBreak:
                return None
            if value is not None:
                return value

    def ev_quit(self, event: tcod.event.Quit) -> Optional[T]:
        return self._current_state.cmd_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:

        # Check if our input is in the MOVE_KEYS library.
        if event.sym in CommandLibrary.MOVE_KEYS:
            return self._current_state.cmd_move(*CommandLibrary.MOVE_KEYS[event.sym])

        try:
            # If not, first try checking the current state's command library...
            if event.sym in CommandLibrary.COMMAND_KEYS[self._current_state.name]:
                commands = CommandLibrary.COMMAND_KEYS[self._current_state]
                command = getattr(self._current_state, f"cmd_{commands[event.sym]}")
                return command()

        except KeyError:
            # ... failing that, try a DEFAULT command.
            if event.sym in CommandLibrary.COMMAND_KEYS['DEFAULT']:
                commands = CommandLibrary.COMMAND_KEYS['DEFAULT']
                command = getattr(self._current_state, f"cmd_{commands[event.sym]}")
                return command()

        else:
            # Oops! No valid commands - return None.
            return None
