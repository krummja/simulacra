from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from engine.areas import Area
from engine.components import Equipment, Inventory, Physics, initialize_character_stats
from config import STAGE_HEIGHT, STAGE_WIDTH
from engine.geometry import Rect
from engine.entities import Player
from engine.rendering import update_fov
from content.factories.factory_service import FactoryService
from content.factories.area_factory import AreaFactory

from engine.tiles.tile import Tile

from graph_engine.generator import Generator

if TYPE_CHECKING:
    from engine.model import Model


def test_area(model: Model) -> Area:

    width: int = STAGE_WIDTH
    height: int = STAGE_HEIGHT

    area = Area(model, width, height)
    area.uid = 'test_forest'

    bare_floor = Tile(
        uid='bare_floor',
        char=ord(" "),
        move_cost=1,
        transparent=True,
        color=(0, 0, 0),
        bg=(42, 42, 42)
        )

    area.area_model.tiles[...] = bare_floor

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
