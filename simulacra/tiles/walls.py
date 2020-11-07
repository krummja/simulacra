from __future__ import annotations
from typing import TYPE_CHECKING

from tile import Tile
from hues import COLOR
from tiles.font_map import font_map


styles = {
    'bare': {
        'foreground': COLOR['slate gray'],
        'background': COLOR['nero']
        },
    'window': {
        'foreground': COLOR['light cyan'],
        'background': COLOR['dark chocolate']
        },
    'door': {
        'foreground': COLOR['chocolate'],
        'background': COLOR['dark chocolate']
        }
    }

walls = {
    'bare': {
        'bricks_01': Tile(
            move_cost=0,
            transparent=False,
            char=font_map['bricks_01'],
            color=styles['bare']['foreground'],
            bg=styles['bare']['background'],
            )
        }
    }
