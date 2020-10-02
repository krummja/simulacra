from __future__ import annotations  # type: ignore

from content.tiles import font_map
from engine.hues import COLOR
from engine.tile import Tile

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
            ),
        'bricks_02': Tile(
            move_cost=0,
            transparent=False,
            char=font_map['bricks_02'],
            color=styles['bare']['foreground'],
            bg=styles['bare']['background'],
            ),
        'beveled_01': Tile(
            move_cost=0,
            transparent=False,
            char=font_map['beveled_03'],
            color=styles['bare']['foreground'],
            bg=styles['bare']['background'],
            ),
        'window_01': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['window_01'],
            color=styles['window']['foreground'],
            bg=styles['window']['background']
            ),
        'window_02': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['window_02'],
            color=styles['window']['foreground'],
            bg=styles['window']['background']
            ),
        'door_01': Tile(
            move_cost=2,
            transparent=True,
            char=font_map['door_01'],
            color=styles['door']['foreground'],
            bg=styles['door']['background']
            ),
        'barrel': Tile(
            move_cost=0,
            transparent=True,
            char=font_map['barrel_01'],
            color=styles['door']['foreground'],
            bg=styles['door']['background']
            ),
        }
    }
