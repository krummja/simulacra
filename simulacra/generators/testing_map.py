from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING
from tile import Tile
from hues import COLOR
from data.tiles.floors import *
from data.tiles.walls import *
from room import Room
from rendering import update_fov
from components.stats import initialize_character_stats
from components.physics import Physics
from components.inventory import Inventory
from player import Player
from area import Area

from tile import tile_graphic

if TYPE_CHECKING:
    from model import Model


testing_tile = Tile('', 1, False, ord("#"), (255, 0, 0), COLOR['nero'])


def testing_area(model: Model) -> Area:
    area = Area(model, 256, 256)
    area.uid = 'test_area'
    
    test_room = Room(1, 1, 100, 100)
    area.area_model.tiles[test_room.inner] = floors['bare']['blank']
    area.area_model.tiles[10, 10] = testing_tile
    
    player = create_character(area, test_room)
    player.noun_text = "administrator"
    
    model.area_data.register(area)
    model.area_data.current_area.player = player
    
    update_fov(area)
    return area


def create_character(area: Area, room: Room) -> Player:
    player = Player(area[room.center])
    player.register_component(initialize_character_stats())
    player.register_component(Inventory())
    player.register_component(Physics(weight=10.0))
    return player


