from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from engine.areas import Area
from engine.components import Equipment, Inventory, Physics, initialize_character_stats
from config import STAGE_HEIGHT, STAGE_WIDTH
from engine.geometry import Rect
from engine.entities import Player
from engine.rendering import update_fov
from content.factories.factory_service import FactoryService
from content.factories.area_factory import AreaFactory
from content.architect.dungeon import DungeonGenerator
from content.architect.graph_generator import GraphGenerator

from graph_engine.generator import Generator

if TYPE_CHECKING:
    from engine.model import Model


factory_service = FactoryService()


def test_forest(model: Model) -> Area:

    width: int = STAGE_WIDTH
    height: int = STAGE_HEIGHT

    area = Area(model, width, height)
    area.uid = 'test_forest'

    factory_service.model = model
    tile_factory = factory_service.tile_factory

    area_factory = AreaFactory(area, max_rooms=40, min_size=8, max_size=24)
    area = area_factory.generate()

    # w = area.width
    # h = area.height

    # generator = GraphGenerator(w, h)
    # generator.generate_nodes_in_radius(30, 10, 30, 50)

    # area.area_model.tiles[...] = tile_factory.build('blank')

    # center = (150, 150)
    # map_data = np.zeros((width, height), dtype=np.int)
    # rect1 = Rect.from_edges(
    #     left=center[0]-5,
    #     top=center[1]-5,
    #     right=center[0]+5,
    #     bottom=center[1]+5
    #     )

    # map_data[rect1.outer] = 1
    # map_data[rect1.inner] = 2

    # area.area_model.tiles.T[map_data == 1] = tile_factory.build('test2')
    # area.area_model.tiles.T[map_data == 2] = tile_factory.build('test1')

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
