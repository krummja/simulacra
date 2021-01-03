from __future__ import annotations
from typing import Dict

from content.tiles.tile_defs import TileType

FOREST_FLOOR = (25, 40, 40)
INTERIOR_FLOOR = (60, 60, 60)

wall_tiles: Dict[str, int] = {
    'brick_1': 57376,
    'brick_2': 57377,
    'brick_3': 57378,
    'brick_4': 57379,
    'brick_5': 57380,
    'brick_6': 57381,
    'brick_wall_L': 57376,
    'brick_wall': 57377,
    'brick_wall_R': 57378,
    'brick_wall_BL': 57379,
    'brick_wall_BR': 57380,
    'slab_1': 57392,
    'slab_2': 57393,
    'window_1': 57408,
    }

brick_left = {
    'uid': 'brick_wall_L',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_L'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_right = {
    'uid': 'brick_wall_R',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_R'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_bot_left = {
    'uid': 'brick_wall_BL',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_BL'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_bot_right = {
    'uid': 'brick_wall_BR',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_BR'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_wall = {
    'uid': 'brick_wall',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

wall_templates = {
    brick_left['uid']: brick_left,
    brick_right['uid']: brick_right,
    brick_bot_left['uid']: brick_bot_left,
    brick_bot_right['uid']: brick_bot_right,
    brick_wall['uid']: brick_wall,
}
