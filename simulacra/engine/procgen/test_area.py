from __future__ import annotations  # type: ignore
from typing import Iterator, List, Tuple, Type, TYPE_CHECKING

import random

import numpy as np
from numpy import ndarray
import tcod

from engine.actions import ai, Action
from engine.character.player import Player
from engine.character import Character
from engine.procgen import process_map
from engine.character.neutral import *
from engine.area import *
from engine.tile import *
from engine.graphic import *
from engine.hues import COLOR
from engine.model import Model
from engine.procgen.room import Room

from content.tiles.floors import *
from content.tiles.walls import *
from content.tiles.forest import *

if TYPE_CHECKING:
    from engine.actor import Actor
    from engine.location import Location
    from engine.model import Model


def roll_asset(area: Area, asset: Dict[str, Dict[str, Tile]], threshold: int):
    for x in range(area.width):
        for y in range(area.height):
            roll = random.randint(0, 100)
            if roll < threshold:
                area.tiles[y, x] = asset
    return area

data_path = './simulacra/engine/procgen/map_test.csv'
BASE_MAP = np.genfromtxt(data_path, delimiter=',', dtype=str)

rules = [
    ('.', floors['bare']['wood']),
    ('W', walls['bare']['bricks_01']),
    ('_', walls['bare']['window_01']),
    ('|', walls['bare']['window_02']),
    ('b', walls['bare']['beveled_01']),
    ('B', walls['bare']['barrel']),
    ('D', walls['bare']['door_01']),
    ('p', basic_forest['paving_stones_01']),
    ('P', basic_forest['paving_stones_02']),
    ('G', basic_forest['gravel_01']),
]

def test_area(model: Model) -> Area:
    area = Area(model, 256, 256)

    test_room = Room(20, 20, 20, 20)
    test_combat_area = Room(50, 50, 20, 20)
    area.tiles[...] = basic_forest['ground_01']

    roll_asset(area, basic_forest['flowers_01'], 5)
    roll_asset(area, basic_forest['flowers_02'], 5)
    roll_asset(area, basic_forest['tree_01'], 20)
    roll_asset(area, basic_forest['clutter_01'], 10)
    roll_asset(area, basic_forest['ground_02'], 10)
    roll_asset(area, basic_forest['rock_01'], 2)
    roll_asset(area, basic_forest['rock_02'], 2)
    process_map(area, BASE_MAP, rules)

    area.player = Player.spawn(area[test_room.center], ai_cls=ai.PlayerControl)

    test_room.place_npcs(area)
    test_combat_area.place_hostiles(area)
    for actor in area.actors:
        actor.character.combat_flag = True
    print(area.actors)

    area.update_fov()

    return area