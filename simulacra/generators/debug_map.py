from __future__ import annotations
from typing import Dict, TYPE_CHECKING

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

    debug_room = Room(20, 20, 20, 20)
    area.area_model.tiles[...] = walls['bare']['bricks_01']
    area.area_model.tiles[debug_room.inner] = floors['bare']['wood']

    area.player = Player(area[debug_room.center])
    area.player.noun_text = "test player"

    update_fov(area)

    return area
