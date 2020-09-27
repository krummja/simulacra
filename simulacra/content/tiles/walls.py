from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.tile import Tile
from engine.hues import COLOR
from content.tiles import font_map

styles = {
    'bare': {
        'foreground': COLOR['saddle brown'],
        'background': COLOR['nero']
    },
    'window': {
        'foreground': COLOR['light cyan'],
        'background': COLOR['burly wood']
    }
}

walls = {
    'bare': {        
        'bricks_01': Tile(
            move_cost=0,
            transparent=False,
            char=font_map['bricks_01'], 
            fg=styles['bare']['foreground'], 
            bg=styles['bare']['background'],
        ),
        'bricks_02': Tile(
            move_cost=0,
            transparent=False,
            char=font_map['bricks_02'], 
            fg=styles['bare']['foreground'], 
            bg=styles['bare']['background'],
        ),
        'window_01': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['checkered_01'],
            fg=styles['window']['foreground'],
            bg=styles['window']['background']
        )
    }
}