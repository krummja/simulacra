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
from generators.dungeon import DungeonGenerator

from factories.area_factory import AreaFactory

from factories.factory_service import FactoryService

if TYPE_CHECKING:
    from model import Model


factory_service = FactoryService()


def test_forest(model: Model) -> Area:
    width: int = STAGE_WIDTH
    height: int = STAGE_HEIGHT
    
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
    generator.generate_nodes_in_radius(30, 10, 30, 50)
    
    area.area_model.tiles.T[generator.map_data == 1] = tile_factory.build('test2')
    area.area_model.tiles.T[generator.map_data == 2] = tile_factory.build('test')
    
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