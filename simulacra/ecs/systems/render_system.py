from __future__ import annotations
from typing import TYPE_CHECKING
from collections import defaultdict

from .system import System
from simulacra.core.options import *
from simulacra.utils.render_utils import *

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from simulacra.core.rendering.tile_grid import TileGrid


def draw_box(console, x, y, w, h):
    # upper border
    border = '┌' + '─' * (w) + '┐'
    console.puts(x - 1, y - 1, border)
    # sides
    for i in range(h):
        console.puts(x - 1, y + i, '│')
        console.puts(x + w, y + i, '│')
    # lower border
    border = '└' + '─' * (w) + '┘'
    console.puts(x - 1, y + h, border)


class RenderSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE'   ])

    def render_visible_entities(self):
        entities = defaultdict(list)

        for entity in self._query.result:
            if not (0 <= entity['POSITION'].x < STAGE_PANEL_WIDTH and
                    0 <= entity['POSITION'].y < STAGE_PANEL_HEIGHT):
                continue
            entities[entity['POSITION'].xy].append(entity['RENDERABLE'])

        for (x, y), graphics in entities.items():
            g = min(graphics)
            self.draw_stage_glyph(x, y, g, layer=1)

    def render_visible_tiles(self, grid: TileGrid) -> None:
        camera_bounds = self._game.camera.camera_bounds
        for x in range(camera_bounds.left, camera_bounds.right):
            for y in range(camera_bounds.top, camera_bounds.bottom):
                glyph = grid.tiles[x, y]['TILE']
                self.draw_stage_glyph(x, y, glyph, layer=0)

    def draw_stage_glyph(self, x, y, glyph, layer=0):
        console = self._game.renderer.root_console
        console.layer(layer)
        console.color(glyph.fg)

        x, y = tile_to_pixel(*cell_to_tile(x, y))
        console.put(x, y, glyph.char)

    def render(self) -> None:
        self._game.renderer.clear()
        self.render_visible_tiles(self._game.area.current_area.grid)
        self.render_visible_entities()

        console = self._game.renderer.root_console
        #! for debugging /////////////////////////////////////////////////////////////////
        draw_box(console, 1, STAGE_PANEL_HEIGHT+1, STAGE_PANEL_WIDTH-2, LOG_PANEL_HEIGHT-2)
        draw_box(console, STAGE_PANEL_WIDTH+1, 1, SIDE_PANEL_WIDTH-2, CONSOLE_HEIGHT-2)
        #! for debugging /////////////////////////////////////////////////////////////////

        offset = 3

        width, height = tile_to_pixel(*cell_to_tile(STAGE_WIDTH, STAGE_HEIGHT))
        console.puts(width + offset, 2, "player pos: " + str(self._game.player.position))

        cell_pos = tile_to_pixel(*cell_to_tile(*self._game.player.position))
        console.puts(width + offset, 3, "cell pos:   " + str(cell_pos))

        pixel_pos = cell_pos[0] * 4, cell_pos[1] * 8
        console.puts(width + offset, 4, "pixel pos:  " + str(pixel_pos))


    def update(self, dt) -> None:
        self.render()

