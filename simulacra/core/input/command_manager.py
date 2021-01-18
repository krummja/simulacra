from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.event import KeyboardEvent

from ..manager import Manager
from .commands import commands
from .input_domain import InputDomain

if TYPE_CHECKING:
    from ..game import Game


class CommandManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._commands = {}
        self._domain_stack = [InputDomain.DEFAULT]
        self._input_stack = []

        for command in commands:
            self.register_command(command)

    def on_input_event(self, event: KeyboardEvent):
        self._input_stack.append(event)

    def get_next_command(self):
        try:
            evt = self._input_stack.pop(-1)
            return self.get_command_for_input_event(evt)
        except IndexError:
            return None

    def push_domain(self, domain):
        self._domain_stack.append(domain)

    def pop_domain(self, domain):
        self._domain_stack.remove(domain)

    def get_domain_commands(self, domain):
        try:
            return self._commands[domain]
        except KeyError:
            return []

    def get_command_for_input_event(self, event: KeyboardEvent):
        for _, domain in enumerate(self._domain_stack):
            cmds = self.get_domain_commands(domain)
            cmd = next(filter(lambda cmd: cmd == event.sym, cmds), None)
            if cmd:
                return cmd

    def register_command(self, command):
        try:
            self._commands[command.domain].append(command)
        except KeyError:
            self._commands[command.domain] = [command]
