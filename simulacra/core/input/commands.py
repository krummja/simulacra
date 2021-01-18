from __future__ import annotations
from typing import Dict, Tuple, List

import tcod

from .input_domain import InputDomain


class Command:
    def __init__(self, **data) -> None:
        self.domain = data['domain']
        self.name = data['name']
        self.event = data['event']

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.event == other



def cmd(domain, name, event) -> Command:
    return Command(**{
        'domain': domain,
        'name': name,
        'event': event
        })


commands: List[Command] = [
    #   DEFAULT                   COMMAND             EVENT
    cmd(InputDomain.DEFAULT,      'confirm',          tcod.event.K_RETURN),
    cmd(InputDomain.DEFAULT,      'exit',             tcod.event.K_ESCAPE),
    ]


class CommandLibrary:

    COMMANDS = [
        "equipment",
        "inventory",
        "pickup",
        "escape",
        "confirm",
        "examine"
        ]

    COMMAND_KEYS: Dict[int, str] = {
        tcod.event.K_e: "equipment",
        tcod.event.K_i: "inventory",
        tcod.event.K_g: "pickup",
        tcod.event.K_ESCAPE: "escape",
        tcod.event.K_RETURN: "confirm",
        tcod.event.K_KP_ENTER: "confirm",
        tcod.event.K_l: "examine",
        }

    MOVE_KEYS: Dict[int, Tuple[int, int]] = {
        # Arrow keys.
        tcod.event.K_LEFT: (-1, 0),
        tcod.event.K_RIGHT: (1, 0),
        tcod.event.K_UP: (0, -1),
        tcod.event.K_DOWN: (0, 1),
        tcod.event.K_HOME: (-1, -1),
        tcod.event.K_END: (-1, 1),
        tcod.event.K_PAGEUP: (1, -1),
        tcod.event.K_PAGEDOWN: (1, 1),
        tcod.event.K_PERIOD: (0, 0),
        # Numpad keys.
        tcod.event.K_KP_1: (-1, 1),
        tcod.event.K_KP_2: (0, 1),
        tcod.event.K_KP_3: (1, 1),
        tcod.event.K_KP_4: (-1, 0),
        tcod.event.K_KP_5: (0, 0),
        tcod.event.K_CLEAR: (0, 0),
        tcod.event.K_KP_6: (1, 0),
        tcod.event.K_KP_7: (-1, -1),
        tcod.event.K_KP_8: (0, -1),
        tcod.event.K_KP_9: (1, -1),
        }
