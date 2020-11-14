from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
import random
import numpy as np

from tiles.floors import *
from tiles.walls import *
from area import Area
from rendering import update_fov
from player import Player
from room import Room

if TYPE_CHECKING:
    from tile import Tile
    from model import Model


def roll_asset(area: Area, asset: Dict[str, Dict[str, Tile]], threshold: int):
    for x in range(area.width):
        for y in range(area.height):
            roll = random.randint(0, 100)
            if roll < threshold:
                area.area_model.tiles[y, x] = asset
    return area


def debug_area(model: Model) -> Area:
    area = Area(model, 120, 120)
    area.ident = 'test area'

    debug_room = Room(20, 20, 20, 20)
    side_room = Room(60, 60, 20, 20)
    area.area_model.tiles[...] = walls['bare']['bricks_01']
    area.area_model.tiles[debug_room.inner] = floors['bare']['wood']
    area.area_model.tiles[side_room.inner] = floors['bare']['wood']

    t_start = debug_room.center
    t_end = debug_room.center

    area.area_model.tiles[tcod.line_where(*t_start, *t_end)] = floors['bare']['wood']

    model.area_data.register(area)

    player = Player(area[debug_room.center])
    player.noun_text = "test player"
    model.area_data.current_area.player = player
    model.entity_data.register(player)

    update_fov(area)

    return area
