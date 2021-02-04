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
            all_of=[ 'RENDERABLE',
                     'SPRITE'     ])

    def render_tile(self, x, y):
        world = self.game.camera.screen_to_world(x, y)
        if not self.game.camera.is_in_view(world['x'], world['y']):
            return

        x, y = tile_from_subtile(*subtile_from_cell(x, y))
        tile = self.area_grid.ground[world['x'], world['y']]

        if self.area_grid.visible[world['x'], world['y']]:
            self.console.color(0xFFFFFFFF)
        elif self.area_grid.explored[world['x'], world['y']]:
            self.console.color(0xFF888888)
        else:
            self.console.color(0xFF000000)

        self.console.layer(0)
        self.console.put(self.x_offset + x, self.y_offset + y, tile['RENDERABLE'].char)

    def render_entity(self, x, y):
        entities = defaultdict(list)
        world = self.game.camera.screen_to_world(x, y)
        if not self.game.camera.is_in_view(world['x'], world['y']):
            return

        for entity in self._query.result:
            entities[entity['POSITION'].xy].append(entity['RENDERABLE'])

        if entities[world['x'], world['y']]:
            graphic = min(entities[world['x'], world['y']])
            self.console.layer(1)
            self.console.color(0xFFFFFFFF)
            self.console.put(self.x_offset + (x * 4), self.y_offset + (y * 2) - 1, graphic.char)

    def render(self) -> None:
        self.game.renderer.clear()
        for x in range(self.game.camera.width):
            for y in range(self.game.camera.height):
                self.render_tile(x, y)
                self.render_entity(x, y)

    def update(self, dt) -> None:
        self.render()
