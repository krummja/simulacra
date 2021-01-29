from __future__ import annotations
from typing import TYPE_CHECKING
from collections import defaultdict

from .system import System
from simulacra.core.options import *
from simulacra.utils.render_utils import *

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from simulacra.core.rendering.tile_grid import TileGrid


class RenderSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE'   ])

        self._tiles = self.ecs.create_query(
            all_of=[ 'TILE' ])

    def render_entity(self, x, y):
        entities = defaultdict(list)
        world = self._game.camera.screen_to_world(x, y)
        console = self._game.renderer.root_console

        for entity in self._query.result:
            if not (0 <= entity['POSITION'].x < STAGE_SIZE and
                    0 <= entity['POSITION'].y < STAGE_SIZE):
                continue
            entities[entity['POSITION'].xy].append(entity['RENDERABLE'])

        if entities[world['x'], world['y']]:
            graphic = min(entities[world['x'], world['y']])
            console.layer(1)
            console.color(0xFFFFFFFF)
            x, y = tile_from_subtile(*subtile_from_cell(x, y))
            console.put(x, y, graphic.char)

    def render_tile(self, x, y):
        world = self._game.camera.screen_to_world(x, y)
        if not self._game.camera.is_in_view(world['x'], world['y']):
            return
        console = self._game.renderer.root_console
        tile = self._game.area.current_area.grid.tiles[world['x'], world['y']]['TILE']
        console.layer(0)
        console.color(tile.fg)
        x, y = tile_from_subtile(*subtile_from_cell(x, y))
        console.put(x, y, tile.char)

    def render(self) -> None:
        self._game.renderer.clear()
        for x in range(self._game.camera.width):
            for y in range(self._game.camera.height):
                self.render_tile(x, y)
                self.render_entity(x, y)

    def update(self, dt) -> None:
        self.render()

