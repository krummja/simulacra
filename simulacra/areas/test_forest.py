from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
import random

from hues import COLOR
from data.tile_defs import *
from area import Area
from player import Player
from components.stats import initialize_character_stats
from components.physics import Physics
from components.inventory import Inventory
from components.equipment import Equipment
from rendering import update_fov
from tile import Tile
from room import Room

from factories.area_factory import AreaFactory

from factories.factory_service import FactoryService

if TYPE_CHECKING:
    from model import Model


factory_service = FactoryService()


def test_forest(model: Model) -> Area:
    width: int = 300
    height: int = 300
    
    area = Area(model, width, height)
    area.uid = 'test_forest'
    
    factory_service.model = model
    tile_factory = factory_service.tile_factory
    
    area_factory = AreaFactory(area, 40, 20, 8)
    area = area_factory.generate()
    
    player = Player("Aulia Inuicta", area[8, 14])
    player.register_component(initialize_character_stats())
    player.register_component(Physics(weight=10.0))
    player.register_component(Equipment())
    player.register_component(Inventory())
    
    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)
    
    update_fov(area)
    
    return area