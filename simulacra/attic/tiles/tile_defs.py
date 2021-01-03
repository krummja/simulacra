from __future__ import annotations
from typing import Dict
from enum import Enum

color_list = [
    (25, 40, 40),
    (60, 60, 60),
    (100, 100, 60),
    (50, 140, 100),
    (135, 100, 70),
    (135, 100, 70),
    (100, 60, 40),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (100, 100, 100),
    (150, 150, 150),
    (0, 0, 0),
    (100, 150, 30),
    (0, 0, 0),
    (0, 0, 0)
    ]

door_tiles: Dict[str, int] = {
    'door_open': 57440,
    'door_closed': 57441,
    'stairs_1': 57442,
    }

all_tiles: Dict[str, int] = {
    'boulder_1': 57344,
    'boulder_2': 57345,
    'boulder_3': 57346,
    'boulder_4': 57347,
    'evergreen_1': 57360,
    'evergreen_2': 57361,
    'evergreen_3': 57362,
    'bushes_1': 57363,
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
    'door_open': 57440,
    'door_closed': 57441,
    'stairs_1': 57442,
    'blank': 0,
    'dirt_1': 57472,
    'dirt_2': 57473,
    'rock_1': 57474,
    'rock_2': 57475,
    'grass_1': 57488,
    'grass_2': 57489,
    'brick_TL': 57504,
    'brick_T': 57505,
    'brick_TR': 57506,
    'blank_stone': 57507,
    'brick_L': 57520,
    'brick_M_1': 57521,
    'brick_R': 57522,
    }

class TileType(Enum):
    Wall = 0
    Floor = 1

FOREST_FLOOR = (25, 40, 40)
INTERIOR_FLOOR = (60, 60, 60)

test_floor1 = {
    'uid': 'test1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    'color': (255, 0, 0),
    'bg': (100, 0, 0)
    }

test_floor2 = {
    'uid': 'test2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    'color': (255, 0, 0),
    'bg': (255, 0, 0)
    }

test_floor3 = {
    'uid': 'test3',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    'color': (0, 0, 0),
    'bg': (50, 50, 200)
    }

test_floor4 = {
    'uid': 'test4',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    'color': (0, 0, 0),
    'bg': (100, 100, 255)
    }

bare_floor = {
    'uid': 'blank',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    'color': (255, 255, 255),
    'bg': FOREST_FLOOR
    }

blank_floor = {
    'uid': 'bare_floor',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    'color': (255, 255, 255),
    'bg': FOREST_FLOOR
    }

blank_stone_floor = {
    'uid': 'blank_stone',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank_stone'],
    'color': (255, 255, 255),
    'bg': INTERIOR_FLOOR
    }

dirt_path = {
    'uid': 'dirt_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['dirt_1'],
    'color': (180, 100, 55),
    'bg': FOREST_FLOOR
    }

door_open = {
    'uid': 'door_open',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': door_tiles['door_open'],
    'color': (100, 60, 40),
    'bg': FOREST_FLOOR
    }

door_closed = {
    'uid': 'door_closed',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': door_tiles['door_closed'],
    'color': (100, 60, 40),
    'bg': FOREST_FLOOR
    }

stairs_down = {
    'uid': 'stairs_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': door_tiles['stairs_1'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

tile_templates = {
    bare_floor['uid']: bare_floor,
    blank_floor['uid']: blank_floor,
    dirt_path['uid']: dirt_path,
    door_open['uid']: door_open,
    door_closed['uid']: door_closed,
    stairs_down['uid']: stairs_down,
    blank_stone_floor['uid']: blank_stone_floor,
    test_floor1['uid']: test_floor1,
    test_floor2['uid']: test_floor2,
    test_floor3['uid']: test_floor3,
    test_floor4['uid']: test_floor4
    }
