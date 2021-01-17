from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.event import KeyboardEvent
from itertools import takewhile, dropwhile

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
        commands = self.get_state_commands(self._game.input.current_state)
        match = lambda cmd: cmd.event == event.sym
        drop = lambda cmd: cmd.event != event.sym
        return min(list(takewhile(match, dropwhile(drop, commands))))

    def get_state_commands(self, state: State):
        match = lambda cmd: cmd.state == state.name
        drop = lambda cmd: cmd.state != state.name
        return list(takewhile(match, dropwhile(drop, self._commands)))
