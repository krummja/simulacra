from __future__ import annotations
from typing import Dict, List, Tuple, TYPE_CHECKING
from collections import defaultdict

from simulacra.utils.debug import debugmethods

from .system import System
from simulacra.core.options import Options

if TYPE_CHECKING:
    from tcod.console import Console
    from ecstremity import Entity
    from simulacra.core.game import Game
    from simulacra.core.rendering.tile_grid import TileGrid


class RenderSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE'   ])

    def render_visible_entities(self, tile_grid: TileGrid) -> None:
        console = self._game.renderer.root_console
        visible_entities: Dict[Tuple[int, int], List[Entity]] = defaultdict(list)
        cam_x, cam_y = self.game.camera.position

        for entity in self._query.result:
            e_x, e_y = entity['POSITION'].x - cam_x, entity['POSITION'].y - cam_y
            if not (0 <= e_x < Options.STAGE_PANEL_WIDTH and
                    0 <= e_y < Options.STAGE_PANEL_HEIGHT):
                continue

            # FIXME: Alright, so we're not correctly setting the tile_grid.visible value
            if not tile_grid.visible[entity['POSITION'].ij]:
                continue

            # TODO: entity['RENDERABLE'].bg = self.get_bg_color(e_x, e_y)

            visible_entities[e_y, e_x].append(entity['RENDERABLE'])

        for ij, graphics in visible_entities.items():
            g = min(graphics)
            console.tiles_rgb[["ch", "fg", "bg"]][ij] = g.char, g.color, g.bg

    def render_visible_tiles(self, tile_grid: TileGrid) -> None:
        console = self._game.renderer.root_console
        viewport, _ = self._game.camera.viewport
        console.tiles_rgb[viewport] = self._game.renderer.select_tile_mask(tile_grid)

    def render(self) -> None:
        self._game.renderer.clear()
        self.render_visible_tiles(self._game.area.current_area.tiles)
        self.render_visible_entities(self._game.area.current_area.tiles)

    def update(self, dt) -> None:
        self.render()
