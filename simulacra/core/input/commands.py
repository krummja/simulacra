from __future__ import annotations

from typing import Dict, Tuple

from bearlibterminal import terminal as blt


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
        blt.TK_LEFT: (-1, 0),
        blt.TK_RIGHT: (1, 0),
        blt.TK_UP: (0, -1),
        blt.TK_DOWN: (0, 1),
        blt.TK_HOME: (-1, -1),
        blt.TK_END: (-1, 1),
        blt.TK_PAGEUP: (1, -1),
        blt.TK_PAGEDOWN: (1, 1),
        blt.TK_PERIOD: (0, 0),
        # Numpad keys.
        blt.TK_KP_1: (-1, 1),
        blt.TK_KP_2: (0, 1),
        blt.TK_KP_3: (1, 1),
        blt.TK_KP_4: (-1, 0),
        blt.TK_KP_5: (0, 0),
        blt.TK_KP_6: (1, 0),
        blt.TK_KP_7: (-1, -1),
        blt.TK_KP_8: (0, -1),
        blt.TK_KP_9: (1, -1),
        }
