from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from area import Area
from components.equipment import Equipment
from components.inventory import Inventory
from components.physics import Physics
from components.stats import initialize_character_stats
from config import STAGE_HEIGHT, STAGE_WIDTH
from factories.area_factory import AreaFactory
from factories.factory_service import FactoryService
from generators.dungeon import DungeonGenerator
from generators.graph_generator import GraphGenerator
from geometry.rect import Rect
from player import Player
from rendering import update_fov

from graph_engine.generator import Generator

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
    center = (150, 150)

    generator = GraphGenerator(w, h)
    generator.generate_nodes_in_radius(30, 10, 30, 50)

    map_data = np.zeros((width, height), dtype=np.int)
    rect1 = Rect.from_edges(left=center[0]-5,
                            right=center[0]+5,
                            top=center[1]-5,
                            bottom=center[1]+5)

    rect2 = Rect.from_edges(left=rect1.right + 1,
                            right=rect1.right + rect1.width + 1,
                            top=rect1.top,
                            bottom=rect1.bottom)

    map_data[rect1.outer] = 1
    map_data[rect1.inner] = 2
    map_data[rect2.outer] = 3
    map_data[rect2.inner] = 4

    area.area_model.tiles.T[map_data == 1] = tile_factory.build('test2')
    area.area_model.tiles.T[map_data == 2] = tile_factory.build('test1')
    area.area_model.tiles.T[map_data == 3] = tile_factory.build('test4')
    area.area_model.tiles.T[map_data == 4] = tile_factory.build('test3')

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
