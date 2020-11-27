from __future__ import annotations
from typing import TYPE_CHECKING

from tile import Tile
from hues import COLOR
from tiles.font_map import font_map


styles = {
    'bare': {
        'foreground': COLOR['nero'],
        'background': COLOR['nero'],
        }
    }

floors = {
    'bare': {
        'blank': Tile(
            move_cost=1,
            transparent=True,
            char=font_map['blank'],
            color=styles['bare']['foreground'],
            bg=styles['bare']['background'],
            ),
        'wood': Tile(
            move_cost=1,
            transparent=True,
            char=font_map['wood_01'],
            color=styles['bare']['foreground'],
            bg=styles['bare']['background'],
            ),
        },
    }
