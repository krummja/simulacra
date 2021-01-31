from __future__ import annotations
from typing import Type, TYPE_CHECKING
from collections import defaultdict

from .system import System
from simulacra.core.options import *
from simulacra.utils.render_utils import *

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from ecstremity import Component


class RenderSystem(System):
    x_offset = (CONSOLE_WIDTH - STAGE_PANEL_WIDTH) // 2
    y_offset = 1

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.console = self.game.renderer.root_console
        self.area_grid = self.game.area.current_area.grid

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE',
                      'OBSTACLE'    ])

        self._tiles = self.ecs.create_query(
            all_of=[ 'TILE' ])

    def render_tile(self, x, y):
        world = self.game.camera.screen_to_world(x, y)
        if not self.game.camera.is_in_view(world['x'], world['y']):
            return

        tile = self.area_grid.ground[world['x'], world['y']]
        self.draw_to_stage(x, y, tile['RENDERABLE'], layer=0)

    def render_entity(self, x, y):
        entities = defaultdict(list)
        for entity in self._query.result:
            entities[entity['POSITION'].xy].append(entity['RENDERABLE'])

        world = self.game.camera.screen_to_world(x, y)
        if entities[world['x'], world['y']]:
            graphic = min(entities[world['x'], world['y']])
            self.draw_to_stage(x, y, graphic, layer=1)

    def render_obstacle(self, x, y):
        world = self.game.camera.screen_to_world(x, y)
        if not self.game.camera.is_in_view(world['x'], world['y']):
            return
        if isinstance(self.area_grid.obstacle[world['x'], world['y']], int):
            return
        obstacle = self.area_grid.obstacle[world['x'], world['y']]
        self.draw_to_stage(x, y, obstacle, layer=1)

    def draw_to_stage(
            self,
            x: int,
            y: int,
            target: Type[Component],
            layer: int = 0
        ) -> None:
        self.console.layer(layer)
        self.console.color(0xFFFFFFFF)
        x, y = tile_from_subtile(*subtile_from_cell(x, y))
        self.console.put(self.x_offset + x, self.y_offset + y, target.char)

    def render(self) -> None:
        self.game.renderer.clear()
        for x in range(self.game.camera.width):
            for y in range(self.game.camera.height):
                self.render_tile(x, y)
                self.render_entity(x, y)
                self.render_obstacle(x, y)

    def update(self, dt) -> None:
        self.render()

