from __future__ import annotations

from typing import TYPE_CHECKING

from config import STAGE_HEIGHT, STAGE_WIDTH
from content.factories.area_factory import AreaFactory
from content.areas.area_engine import AreaEngine, AreaPainter
from engine.areas import Area
from engine.components import (Equipment, Inventory, Physics,
                               initialize_character_stats)
from engine.entities.player import Player
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

    factory = AreaFactory(area)
    factory.generate()

    # generator = AreaPainter(AreaEngine(area))
    # generator.engine.generate()
    # generator.paint_owners()

    player = Player("Aulia Inuicta", area[128, 128])
    player.register_component(initialize_character_stats())
    player.register_component(Physics(weight=10.0))
    player.register_component(Equipment())
    player.register_component(Inventory())

    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)

    update_fov(area)

    return area
