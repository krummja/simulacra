from __future__ import annotations
from typing import Dict

from content.tiles.tile_defs import TileType

FOREST_FLOOR = (25, 40, 40)
INTERIOR_FLOOR = (60, 60, 60)

terrain_tiles: Dict[str, int] = {
    'boulder_1': 57344,
    'boulder_2': 57345,
    'boulder_3': 57346,
    'boulder_4': 57347,
    'evergreen_1': 57360,
    'evergreen_2': 57361,
    'evergreen_3': 57362,
    'bushes_1': 57363,
    'rock_1': 57474,
    'rock_2': 57475,
    'grass_1': 57488,
    'grass_2': 57489,
    }

evergreen_1 = {
    'uid': 'evergreen_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['evergreen_1'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

evergreen_2 = {
    'uid': 'evergreen_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['evergreen_2'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

evergreen_3 = {
    'uid': 'evergreen_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['evergreen_3'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

boulder_1 = {
    'uid': 'boulder_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['boulder_1'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

boulder_2 = {
    'uid': 'boulder_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['boulder_2'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

boulder_3 = {
    'uid': 'boulder_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['boulder_3'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

boulder_4 = {
    'uid': 'boulder_4',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': terrain_tiles['boulder_4'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

rock_1 = {
    'uid': 'rock_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': terrain_tiles['rock_1'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

rock_2 = {
    'uid': 'rock_2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': terrain_tiles['rock_2'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

grass_1 = {
    'uid': 'grass_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': terrain_tiles['grass_1'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

grass_2 = {
    'uid': 'grass_2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': terrain_tiles['grass_2'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

terrain_templates = {
    evergreen_1['uid']: evergreen_1,
    evergreen_2['uid']: evergreen_2,
    evergreen_3['uid']: evergreen_3,
    boulder_1['uid']: boulder_1,
    boulder_2['uid']: boulder_2,
    boulder_3['uid']: boulder_3,
    boulder_4['uid']: boulder_4,
    grass_1['uid']: grass_1,
    grass_2['uid']: grass_2,
    rock_1['uid']: rock_1,
    rock_2['uid']: rock_2,
}

