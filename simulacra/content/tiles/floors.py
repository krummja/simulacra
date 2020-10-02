from __future__ import annotations  # type: ignore

from engine.tile import Tile
from engine.hues import COLOR
from content.tiles import font_map


styles = {
    'bare': {
        'foreground': COLOR['dark chocolate'],
        'background': COLOR['nero']
        },
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
