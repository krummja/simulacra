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


class InputController(Manager):
    """Inherits TCOD's EventDispatch to provide basic input mapping.
    Commands are handled separately in the CommandManager.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self._current_screen = game.screens.current_screen

    def handle_input(self) -> Optional[Callable[[], Optional[T]]]:
        key = self.game.renderer.root_console.read()
        try:
            command = self.key_command_lookup(key)
        except StateBreak:
            return None
        if command is not None:
            return command

    def key_command_lookup(self, key):
        if key in CommandLibrary.MOVE_KEYS:
            return self._current_screen.cmd_move(*CommandLibrary.MOVE_KEYS[key])
        try:
            if key in CommandLibrary.COMMAND_KEYS[self._current_screen.name]:
                commands = CommandLibrary.COMMAND_KEYS[self._current_screen.name]
                command = getattr(self._current_screen, f"cmd_{commands[key]}")
                return command
        except KeyError:
            if key in CommandLibrary.COMMAND_KEYS['DEFAULT']:
                commands = CommandLibrary.COMMAND_KEYS['DEFAULT']
                command = getattr(self._current_screen, f"cmd_{commands[key]}")
                return command
        else:
            return None
