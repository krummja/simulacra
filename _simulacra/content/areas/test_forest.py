from __future__ import annotations

from typing import TYPE_CHECKING

from engine.areas import Area
from engine.components import Equipment, Inventory, Physics, initialize_character_stats
from config import STAGE_HEIGHT, STAGE_WIDTH
from engine.entities import Player
from engine.rendering import update_fov
from content.factories.area_factory import AreaFactory

if TYPE_CHECKING:
    from engine.model import Model


def test_forest(model: Model) -> Area:

    width: int = STAGE_WIDTH
    height: int = STAGE_HEIGHT

    area = Area(model, width, height)
    area.uid = 'test_forest'

    area_factory = AreaFactory(area)
    area_factory.generate()

    player = Player("Aulia Inuicta", area[area_factory.start_tile])
    player.register_component(initialize_character_stats())
    player.register_component(Physics(weight=10.0))
    player.register_component(Equipment())
    player.register_component(Inventory())

    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)

    update_fov(area)

    return area
