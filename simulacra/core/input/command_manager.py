from __future__ import annotations

from itertools import dropwhile, takewhile
from typing import TYPE_CHECKING

from tcod.event import KeyboardEvent

from ..manager import Manager
from .commands import command_library

if TYPE_CHECKING:
    from ..game import Game
    from ..states.state import State


class CommandManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._commands = command_library

    def on_input_event(self, event: KeyboardEvent):
        state_commands = self.get_state_commands(self._game.state.current_state)
        result = list(filter(lambda c: c.event == event.sym, state_commands))
        if len(result) > 0:
            return result[0]
        else:
            pass

    def get_state_commands(self, state: State):
        match = lambda cmd: cmd.state == state.name
        drop = lambda cmd: cmd.state != state.name
        return list(takewhile(match, dropwhile(drop, self._commands)))
