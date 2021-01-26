from __future__ import annotations
from typing import Dict, List, Tuple, TYPE_CHECKING
from collections import defaultdict

from .system import System
from simulacra.core.options import *
from simulacra.utils.geometry import Rect
from simulacra.utils.math_utils import mod

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from simulacra.utils.geometry.array2d import Array2D


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
            if not (0 <= entity['POSITION'].x < (STAGE_PANEL_WIDTH * 2) and
                    0 <= entity['POSITION'].y < (STAGE_PANEL_HEIGHT * 2) + 4):
                continue
            entities[entity['POSITION'].xy].append(entity['RENDERABLE'])

        for (x, y), graphics in entities.items():
            g = min(graphics)
            self.draw_entity_glyph(x, y, g, layer=1)

    def render_visible_tiles(self, array2d: Array2D) -> None:
        camera_bounds = self._game.camera.camera_bounds
        for x in range(camera_bounds.left, camera_bounds.right, 4):
            for y in range(camera_bounds.top, camera_bounds.bottom, 2):
                glyph = array2d[x, y]['TILE']
                self.draw_stage_glyph(x, y, glyph, layer=0)

    def draw_stage_glyph(self, x, y, glyph, layer=0):
        console = self._game.renderer.root_console
        console.layer(layer)
        console.color(glyph.fg)

        camera_bounds = self._game.camera.camera_bounds
        render_offset = self._game.camera.render_offset

        console.put(
            x - camera_bounds.left + render_offset[0],
            y - camera_bounds.top + render_offset[1],
            glyph.char
            )

    def draw_entity_glyph(self, x, y, glyph, layer=1):
        camera_bounds = self._game.camera.camera_bounds
        render_offset = self._game.camera.render_offset

        console = self._game.renderer.root_console
        console.layer(layer)
        console.color(glyph.fg)
        console.put(x - camera_bounds.left + render_offset[0],
                    y - camera_bounds.top + render_offset[1],
                    glyph.char)

    def render(self) -> None:
        self._game.renderer.clear()
        self.render_visible_tiles(self._game.area.current_area.grid)
        self.render_visible_entities()

        #! for debugging /////////////////////////////////////////////////////////////////
        draw_box(self._game.renderer.root_console, 1, STAGE_PANEL_HEIGHT+1, STAGE_PANEL_WIDTH-2, LOG_PANEL_HEIGHT-2)
        draw_box(self._game.renderer.root_console, STAGE_PANEL_WIDTH+1, 1, SIDE_PANEL_WIDTH-2, CONSOLE_HEIGHT-2)
        #! for debugging /////////////////////////////////////////////////////////////////

        self.draw_debugging_overlay()

    def draw_debugging_overlay(self):
        console = self._game.renderer.root_console
        x = self._game.player.position[0]
        y = self._game.player.position[1]
        offset = STAGE_PANEL_WIDTH + 2

        arr = self._game.area.current_area._tiles
        console.puts(offset, 10, "array w: " + str(arr.width))
        console.puts(offset, 11, "array h: " + str(arr.height))

        console.puts(offset, 13, "camera w pos: " + str(self._game.camera.camera_bounds.center))
        console.puts(offset, 14, "camera s pos: " + str(self._game.camera.bounds.center))

        console.puts(offset, 16, "camera bounds")
        console.puts(offset, 17, "---------------------")
        console.puts(offset, 18, "width: " + str(self._game.camera.camera_bounds.width))
        console.puts(offset, 19, "height: " + str(self._game.camera.camera_bounds.height))
        console.puts(offset, 20, "left: " + str(self._game.camera.camera_bounds.left))
        console.puts(offset, 21, "top: " + str(self._game.camera.camera_bounds.top))
        console.puts(offset, 22, "right: " + str(self._game.camera.camera_bounds.right))
        console.puts(offset, 23, "bottom: " + str(self._game.camera.camera_bounds.bottom))

        console.puts(offset, 26, "screen position")
        console.puts(offset, 27, "--------------------")
        console.puts(offset, 28, "x: " + str(self._game.player.position[0]))
        console.puts(offset + 8, 28, "y: " + str(self._game.player.position[1]))

        console.puts(offset, 30, "cell position")
        console.puts(offset, 21, "----------------")
        console.puts(offset, 32, "x: " + str(x // 2))
        console.puts(offset + 8, 32, "y: " + str(y // 2))

        console.puts(offset, 34, "coordinates")
        console.puts(offset, 35, "----------------")
        console.puts(offset, 36, "x: " + str(x // 4))
        console.puts(offset + 8, 36, "y: " + str(y // 2))

    def update(self, dt) -> None:
        self.render()

