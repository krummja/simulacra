from __future__ import annotations
from typing import List

import tcod


class Command:
    def __init__(self, **data) -> None:
        self.state = data['state']
        self.name = data['name']
        self.event = data['event']


def cmd(state, name, event) -> Command:
    return Command(**{
        'state': state,
        'name': name,
        'event': event
        })


command_library: List[Command] = [
    #   STATE           COMMAND             EVENT SYM
    cmd('DEFAULT',      'confirm',          tcod.event.K_RETURN),
    cmd('TEST',         'confirm',          tcod.event.K_RETURN),
    cmd('TEST',         'exit',             tcod.event.K_ESCAPE),
]
