from __future__ import annotations
from typing import Tuple, Dict
from enum import Enum
from hues import COLOR, Colors


wall_tiles: Dict[str, int] = {
    'rock_1': 57344,
    'rock_2': 57345,
    'rock_3': 57346,
    'rock_4': 57347,
    'tree_1': 57360,
    'tree_2': 57361,
    'tree_3': 57362,
    'bushes_1': 57363,
    'brick_1': 57376,
    'brick_2': 57377,
    'brick_3': 57378,
    'brick_4': 57379,
    'brick_5': 57380,
    'brick_6': 57381,
    'slab_1': 57392,
    'slab_2': 57393,
    'window_1': 57408,
}

door_tiles: Dict[str, int] = {
    'door_1': 57440,
    'door_2': 57441,
    'stairs_1': 57442,
}

ground_tiles: Dict[str, int] = {
    'blank': 0,
    'dirt_1': 57472,
    'dirt_2': 57473,
    'rock_1': 57474,
    'rock_2': 57475,
    'grass_1': 57488,
    'grass_2': 57489
}


class TileType(Enum):
    Wall = 0
    Floor = 1

FOREST_FLOOR = (25, 40, 40)

bare_floor = {
    'uid': 'bare_floor',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (255, 255, 255),
    'bg': FOREST_FLOOR
    }

dirt_path = {
    'uid': 'dirt_path',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['dirt_1'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

evergreen_1 = {
    'uid': 'evergreen_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['tree_1'],
    'color': (55, 100, 55),
    'bg': FOREST_FLOOR
    }

evergreen_2 = {
    'uid': 'evergreen_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['tree_2'],
    'color': (55, 100, 55),
    'bg': FOREST_FLOOR
    }

rock_1 = {
    'uid': 'rock_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['rock_1'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

rock_2 = {
    'uid': 'rock_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['rock_2'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

rock_3 = {
    'uid': 'rock_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['rock_3'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

rock_4 = {
    'uid': 'rock_4',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['rock_4'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }


tile_templates = {
    bare_floor['uid']: bare_floor,
    dirt_path['uid']: dirt_path,
    evergreen_1['uid']: evergreen_1,
    evergreen_2['uid']: evergreen_2,
    rock_1['uid']: rock_1,
    rock_2['uid']: rock_2,
    rock_3['uid']: rock_3,
    rock_4['uid']: rock_4,
    }
