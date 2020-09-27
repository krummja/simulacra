from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.tile import Tile
from engine.hues import COLOR
from content.tiles import font_map

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
        'beveled_01': Tile(
            move_cost=0,
            transparent=False,
            char=font_map['beveled_03'], 
            fg=styles['bare']['foreground'], 
            bg=styles['bare']['background'],
        ),
        'window_01': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['window_01'],
            fg=styles['window']['foreground'],
            bg=styles['window']['background']
        ),
        'window_02': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['window_02'],
            fg=styles['window']['foreground'],
            bg=styles['window']['background']
        ),
        'door_01': Tile(
            move_cost=2,
            transparent=True,
            char=font_map['door_01'],
            fg=styles['door']['foreground'],
            bg=styles['door']['background']
        ),
        'barrel': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['barrel_01'],
            fg=styles['door']['foreground'],
            bg=styles['door']['background']
        ),
    }
}