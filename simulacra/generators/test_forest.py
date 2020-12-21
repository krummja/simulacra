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

from factories.factory_service import FactoryService

if TYPE_CHECKING:
    from model import Model


factory_service = FactoryService()


def roll_asset(area: Area, template: str, threshold: int, x=None, y=None):
    _x_range = range(area.width) if x is None else x
    _y_range = range(area.height) if y is None else y

    _x = [x for x in range(area.width)] if x is None else [x]
    _y = [y for y in range(area.height)] if y is None else [y]

    for x in _x:
        for y in _y:
            roll = random.randint(0, 100)
            if roll < threshold:
                area.area_model.tiles[y, x] = factory_service.tile_factory.build(template)
    return area


def test_forest(model: Model) -> Area:
    width: int = 120
    height: int = 120
    
    area = Area(model, width, height)
    area.uid = 'test_forest'
    
    factory_service.model = model
    tile_factory = factory_service.tile_factory
    
    bsp = tcod.bsp.BSP(x=0, y=0, width=width, height=height)
    bsp.split_recursive(
        depth=10,
        min_width=15,
        min_height=15,
        max_horizontal_ratio=2.0,
        max_vertical_ratio=2.0,
        )
    
    area.area_model.tiles[...] = tile_factory.build('bare_floor')
    area = roll_asset(area, 'evergreen_1', 20)
    area = roll_asset(area, 'evergreen_2', 20)
    area.area_model.tiles[30, 0:50] = tile_factory.build('dirt_path')
    area = roll_asset(area, 'rock_1', 20, y=29)
    area = roll_asset(area, 'rock_2', 20, y=29)
    area = roll_asset(area, 'rock_3', 20, y=29)
    area = roll_asset(area, 'rock_4', 20, y=29)
    start_room = Room(20, 20, 20, 20)
    
    # for node in bsp.pre_order():
    #     if node.children:
    #         pass
    #         # node1, node2 = node.children
    #         # Connect Node1, Node2
    #     else:
    #         room = Room(node.x, node.y, node.w, node.h)
    #         area.area_model.tiles[room.inner] = debug_floor
            
    player = Player("Aulia Inuicta", area[start_room.center])
    player.register_component(initialize_character_stats())
    player.register_component(Physics(weight=10.0))
    player.register_component(Equipment())
    player.register_component(Inventory())
    
    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)
    
    update_fov(area)
    
    return area