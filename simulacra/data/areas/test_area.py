from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.world.area import Area

if TYPE_CHECKING:
    from simulacra.core.area_manager import AreaManager


class TestArea(Area):
    name = "TEST"

    def __init__(self, manager: AreaManager) -> None:
        super().__init__(manager)

        default_tile = manager.game.ecs.engine.create_entity()
        default_tile.add('RENDERABLE', {
            'codepoint': self._sprites.get_codepoint('ground', 'tile_1'),
            })
        default_tile.add('TILE', {
            'transparent': True,
            'passable': True,
            'unformed': True,
            })

        wall_left_1 = manager.game.ecs.engine.create_entity()
        wall_left_1.add('RENDERABLE', {
            'codepoint': self._sprites.get_codepoint('wall', 'wall_left_1'),
            })
        wall_left_1.add('TILE', {
            'transparent': False,
            'passable': False,
            'unformed': True,
            })

        wall_right_1 = manager.game.ecs.engine.create_entity()
        wall_right_1.add('RENDERABLE', {
            'codepoint': self._sprites.get_codepoint('wall', 'wall_right_1'),
            })
        wall_right_1.add('TILE', {
            'transparent': False,
            'passable': False,
            'unformed': True,
            })

        wall_bottom_1 = manager.game.ecs.engine.create_entity()
        wall_bottom_1.add('RENDERABLE', {
            'codepoint': self._sprites.get_codepoint('wall', 'wall_bottom_1'),
            })
        wall_bottom_1.add('TILE', {
            'transparent': False,
            'passable': False,
            'unformed': True,
            })

        wall_bottom_2 = manager.game.ecs.engine.create_entity()
        wall_bottom_2.add('RENDERABLE', {
            'codepoint': self._sprites.get_codepoint('wall', 'wall_bottom_2'),
            })
        wall_bottom_2.add('TILE', {
            'transparent': False,
            'passable': False,
            'unformed': True,
            })

        self._grid.transparent[:] = default_tile['TILE'].transparent
        self._grid.ground[:] = default_tile

        self._grid.passable[11, 0:11] = wall_right_1['TILE'].passable
        self._grid.transparent[11, 0:11] = wall_right_1['TILE'].transparent
        self._grid.ground[11, 0:11] = wall_right_1

        self._grid.passable[12, 0:11] = wall_left_1['TILE'].passable
        self._grid.transparent[12, 0:11] = wall_left_1['TILE'].transparent
        self._grid.ground[12, 0:11] = wall_left_1

        self._grid.passable[11, 11] = wall_bottom_2['TILE'].passable
        self._grid.transparent[11, 11] = wall_bottom_2['TILE'].transparent
        self._grid.ground[11, 11] = wall_bottom_2

        self._grid.passable[12, 11] = wall_bottom_1['TILE'].passable
        self._grid.transparent[12, 11] = wall_bottom_1['TILE'].transparent
        self._grid.ground[12, 11] = wall_bottom_1
