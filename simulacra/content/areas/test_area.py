from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from config import STAGE_HEIGHT, STAGE_WIDTH
from content.factories.area_factory import AreaFactory
from content.factories.tile_factory import TileFactory
from engine.areas import Area
from engine.components import (Equipment, Inventory, Physics,
                               initialize_character_stats)
from engine.entities import Player
from engine.geometry import Rect
from engine.rendering import update_fov

if TYPE_CHECKING:
    from engine.model import Model


FOREST_FLOOR = (25, 40, 40)
INTERIOR_FLOOR = (60, 60, 60)


def test_area(model: Model) -> Area:

    width: int = STAGE_WIDTH
    height: int = STAGE_HEIGHT

    area = Area(model, width, height)
    area.uid = 'test_forest'

    tile_factory = TileFactory()
    area_factory = AreaFactory(area=area,
                               max_rooms=50,
                               min_size=16,
                               max_size=32)

    area.area_model.tiles[...] = tile_factory.build('grass_1',
                                                    color=(40, 80, 80),
                                                    bg=FOREST_FLOOR)
    area_factory.generate()

    player = Player("Aulia Inuicta", area[150, 150])
    player.register_component(initialize_character_stats())
    player.register_component(Physics(weight=10.0))
    player.register_component(Equipment())
    player.register_component(Inventory())

    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)

    update_fov(area)

    return area
