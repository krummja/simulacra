from __future__ import annotations
from typing import TYPE_CHECKING
from collections import defaultdict

from simulacra.utils.debug import debugmethods

from .system import System
from simulacra.core.options import Options

if TYPE_CHECKING:
    from tcod.console import Console
    from simulacra.core.game import Game
    from simulacra.core.rendering.tile_grid import TileGrid


@debugmethods
class RenderSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self._actor_query = self.ecs.create_query(
            all_of=[  'ACTOR'     ],
            none_of=[ 'INVISIBLE' ])

        self._renderable_query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE'   ])

    def render_visible_entities(self, tile_grid: TileGrid, console: Console) -> None:
        visible_entities = defaultdict(list)
        cam_x, cam_y = self.game.camera.position

        for entity in self._actor_query.result:
            e_x, e_y = entity['POSITION'].x - cam_x, entity['POSITION'].y - cam_y
            if not (0 <= e_x < Options.SIDE_PANEL_WIDTH and
                    0 <= e_y < Options.SIDE_PANEL_HEIGHT):
                continue
            if not tile_grid.visible[entity['POSITION'].ij]:
                continue
            # TODO: entity['RENDERABLE'].bg = self.get_bg_color(e_x, e_y)
            visible_entities[e_y, e_x].append(entity)



    def render_visible_tiles(self, tile_grid: TileGrid, console: Console) -> None:
        pass

    def render(self) -> None:
        self._game.renderer.clear()
        for entity in self._query.result:
            self._game.renderer.root_console.print(
                entity['POSITION'].x, entity['POSITION'].y, entity['RENDERABLE'].char)

    def update(self, dt) -> None:
        self.render()
