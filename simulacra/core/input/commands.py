from __future__ import annotations
from typing import Dict, Tuple

from bearlibterminal import terminal as blt
import tcod

blt.TK_KP_ENTER


class CommandLibrary:

    COMMAND_KEYS: Dict[str, Dict[int, str]] = {
        'DEFAULT': {
            blt.TK_RETURN: "confirm",
            blt.TK_KP_ENTER: "confirm",
            blt.TK_ESCAPE: "escape",
            },
        'MAIN_MENU': {
            blt.TK_Q: "quit",
            },
        'PLAYER_READY': {
            blt.TK_D: "drop",
            blt.TK_E: "equipment",
            blt.TK_G: "pickup",
            blt.TK_I: "inventory",
            blt.TK_L: "examine",
            }
        }

    MOVE_KEYS: Dict[int, Tuple[int, int]] = {
        # Arrow keys.
        blt.TK_LEFT: (-2, 0),
        blt.TK_RIGHT: (2, 0),
        blt.TK_UP: (0, -1),
        blt.TK_DOWN: (0, 1),
        blt.TK_HOME: (-2, -1),
        blt.TK_END: (-2, 1),
        blt.TK_PAGEUP: (2, -1),
        blt.TK_PAGEDOWN: (2, 1),
        blt.TK_PERIOD: (0, 0),
        # Numpad keys.
        blt.TK_KP_1: (-2, 1),
        blt.TK_KP_2: (0, 1),
        blt.TK_KP_3: (2, 1),
        blt.TK_KP_4: (-2, 0),
        blt.TK_KP_5: (0, 0),
        blt.TK_KP_6: (2, 0),
        blt.TK_KP_7: (-2, -1),
        blt.TK_KP_8: (0, -1),
        blt.TK_KP_9: (2, -1),
        }
