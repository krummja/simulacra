from __future__ import annotations
from typing import Dict, List

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


# A command is a triple (state_name | 'DEFAULT', command_name, event_sym)
command_library: List[Command] = [
    cmd('DEFAULT', 'confirm', tcod.event.K_RETURN),
    cmd('TEST', 'confirm', tcod.event.K_RETURN),
]
