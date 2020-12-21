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

if TYPE_CHECKING:
    from model import Model


bare_floor = Tile(
    move_cost=1,
    transparent=True,
    char=0,
    color=COLOR['dark dark green'],
    bg=COLOR['dark dark green']
    )

debug_floor = Tile(
    move_cost=1,
    transparent=True,
    char=0,
    color=COLOR['light coral'],
    bg=COLOR['light coral']
    )

brick_wall = Tile(
    move_cost = 0,
    transparent=False,
    char=wall_tiles['brick_1'],
    color=COLOR['rosy brown'],
    bg=COLOR['dark dark green']
    )


def test_forest(model: Model) -> Area:
    width: int = 120
    height: int = 120
    
    area = Area(model, width, height)
    area.uid = 'test_forest'
    
    bsp = tcod.bsp.BSP(x=0, y=0, width=width, height=height)
    bsp.split_recursive(
        depth=10,
        min_width=15,
        min_height=15,
        max_horizontal_ratio=2.0,
        max_vertical_ratio=2.0,
        )
    
    area.area_model.tiles[...] = bare_floor

    start_room = Room(20, 20, 20, 20)
    area.area_model.tiles[start_room.outer] = brick_wall
    area.area_model.tiles[start_room.inner] = bare_floor
        
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