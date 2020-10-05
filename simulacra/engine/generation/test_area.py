from __future__ import annotations  # type: ignore
from typing import Dict, TYPE_CHECKING

import random
import numpy as np

from content.tiles.floors import *
from content.tiles.walls import *
from engine.area import Area
from engine.items.door import Door
from engine.player import Player
from engine.actions.behaviors.player_control import PlayerControl

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


data_path = './simulacra/engine/generation/map_test.csv'
BASE_MAP = np.genfromtxt(data_path, delimiter=',', dtype=str)


def test_area(model: Model) -> Area:
    area = Area(model, 256, 256)

    area.tiles[...] = floors['bare']['wood']

    area.tiles[15, 0:15] = walls['bare']['bricks_01']
    area.tiles[15, 16:30] = walls['bare']['bricks_01']

    Door.place(
        char=font_map['door_01'],
        color=COLOR['chocolate'],
        bg=area.get_bg_color(15, 15),
        noun_text="Test Door",
        location=area[15, 15]
        )

    area.player = Player.spawn(
        ord("@"),
        (255, 0, 255),
        (0, 0, 0),
        "Player",
        area[10, 10],
        )
    area.update_fov()

    return area
