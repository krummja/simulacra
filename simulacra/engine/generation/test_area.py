from __future__ import annotations  # type: ignore
from typing import Dict, TYPE_CHECKING

import random
import numpy as np

from content.tiles.floors import *
from content.tiles.walls import *
from content.tiles.forest import *
from engine.area import Area
from engine.generation import process_map, process_doors
from engine.items.door import Door
from engine.player import Player
from engine.npc import NPC
from engine.room import Room
from engine.items.test_item import TestItem

if TYPE_CHECKING:
    from engine.tile import Tile
    from engine.model import Model


def roll_asset(area: Area, asset: Dict[str, Dict[str, Tile]], threshold: int):
    for x in range(area.width):
        for y in range(area.height):
            roll = random.randint(0, 100)
            if roll < threshold:
                area.tiles[y, x] = asset
    return area


data_path = './simulacra/engine/generation/'
BASE_MAP = np.genfromtxt(f"{data_path}map_test.csv", delimiter=',', dtype=str)
DOOR_MAP = np.genfromtxt(f"{data_path}map_test_doors.csv", delimiter=',', dtype=str)
rules = [
    ('.', floors['bare']['wood']),
    ('W', walls['bare']['bricks_01']),
    ('_', walls['bare']['window_01']),
    ('|', walls['bare']['window_02']),
    ('b', walls['bare']['beveled_01']),
    ('B', walls['bare']['barrel']),
    ('p', basic_forest['paving_stones_01']),
    ('P', basic_forest['paving_stones_02']),
    ('G', basic_forest['gravel_01']),
    ]


def test_area(model: Model) -> Area:
    area = Area(model, 256, 256)

    test_room = Room(20, 20, 20, 20)
    area.tiles[...] = basic_forest['ground_01']
    roll_asset(area, basic_forest['tree_01'], 20)
    roll_asset(area, basic_forest['clutter_01'], 10)
    roll_asset(area, basic_forest['ground_02'], 10)
    roll_asset(area, basic_forest['flowers_01'], 5)
    roll_asset(area, basic_forest['flowers_02'], 5)
    roll_asset(area, basic_forest['rock_01'], 2)
    roll_asset(area, basic_forest['rock_02'], 2)
    area = process_map(area, BASE_MAP, rules)
    doors = process_doors(DOOR_MAP)

    for door in doors:
        Door.place(
            char=font_map['door_01'],
            color=COLOR['chocolate'],
            bg=area.get_bg_color(door[1], door[0]),
            noun_text="solid door",
            location=area[door[1], door[0]]
            )

    area.player = Player.spawn(area[test_room.center])
    area.player.noun_text = "test player"

    TestItem.place(ord("$"), (0, 255, 255), area.get_bg_color(32, 32), "test item", area[32, 32])

    NPC.spawn(area[test_room.center[0]+2, test_room.center[1]])

    area.update_fov()

    return area
