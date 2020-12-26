from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
import random

from config import STAGE_WIDTH, STAGE_HEIGHT
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
from generators.graph_generator import GraphGenerator

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
    
    # area_factory = AreaFactory(area, 40, 20, 8)
    # area = area_factory.generate()
    
    area.area_model.tiles[...] = tile_factory.build('blank')
    w = area.width
    h = area.height
    center = (w // 2, h // 2)
    
    generator = GraphGenerator(w, h)
    debug_map = generator.generate(6, 10, 20, 10)
    room_map = generator.generate_rooms()
    area.area_model.tiles[debug_map==1] = tile_factory.build('test4')
    area.area_model.tiles[debug_map==2] = tile_factory.build('test3')
    area.area_model.tiles[room_map==1] = tile_factory.build('test')
    area.area_model.tiles[room_map==2] = tile_factory.build('test2')
    
    player = Player("Aulia Inuicta", area[center])
    player.register_component(initialize_character_stats())
    player.register_component(Physics(weight=10.0))
    player.register_component(Equipment())
    player.register_component(Inventory())
    
    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)
    
    update_fov(area)
    
    return area