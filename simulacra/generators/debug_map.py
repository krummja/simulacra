from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
import random

from data.tiles.floors import *
from data.tiles.walls import *
from area import Area
from rendering import update_fov
from player import Player
from room import Room
from components.attributes import initialize_character_attributes
from components.physics import Physics
from components.inventory import Inventory
from components.equipment import Equipment
from factories.factory_service import FactoryService
from factories.item_factory import ItemFactory
from managers.manager_service import ManagerService
from factories.factory_service import FactoryService

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
    area.uid = 'test_area'

    # TODO: Make a RoomFactory
    debug_room = Room(20, 20, 20, 20)
    side_room = Room(60, 60, 20, 20)

    # TODO: It would be nice to have functions for this - these are really clunky
    area.area_model.tiles[...] = walls['bare']['bricks_01']
    area.area_model.tiles[debug_room.inner] = floors['bare']['blank']
    area.area_model.tiles[side_room.inner] = floors['bare']['blank']

    # TODO: Make a TunnelFactory
    t_start = debug_room.center
    t_end = side_room.center
    t_middle = t_start[0], t_end[1]
    area.area_model.tiles[tcod.line_where(*t_start, *t_middle)] = floors['bare']['blank']
    area.area_model.tiles[tcod.line_where(*t_middle, *t_end)] = floors['bare']['blank']

    # TODO: PlayerFactory will make this easier, of course
    player = Player(area[debug_room.center])
    player.register_component(initialize_character_attributes())
    player.register_component(Inventory())
    player.register_component(Equipment())
    player.register_component(Physics(weight=10.0))
    player.noun_text = "aulia inuicta"

    model.area_data.register(area)
    model.area_data.current_area.player = player
    model.entity_data.register(player)

    factory_service = FactoryService()
    manager_service = ManagerService()
    factory_service.model = model
    character_factory = factory_service.character_factory
    item_factory = factory_service.item_factory

    character_factory.build(
        uid='test_character',
        location=area[debug_room.center[0] + 2, debug_room.center[1] + 2]
        )

    character_factory.build(
        uid='test_character_2',
        location=area[debug_room.center[0] - 2, debug_room.center[1] - 2]
        )
    
    item_factory.build(
        uid='test_item',
        location=area[debug_room.center[0], debug_room.center[1] + 4]
        )

    item_factory.build(
        uid='other_item',
        location=area[debug_room.center[0] - 2, debug_room.center[1] + 4]
        )

    update_fov(area)

    return area
