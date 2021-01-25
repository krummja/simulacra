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
            entities[entity['POSITION'].x, entity['POSITION'].y].append(entity['RENDERABLE'])

        for (x, y), graphics in entities.items():
            g = min(graphics)
            self.draw_stage_glyph(x, y, g, layer=1)

    def render_visible_tiles(self, array2d: Array2D) -> None:
        for x in range(0, STAGE_WIDTH, 2):
            for y in range(0, STAGE_HEIGHT):
                glyph = array2d[x, y]['TILE']
                self.draw_stage_glyph(x, y, glyph, layer=0)

    def draw_stage_glyph(self, x, y, glyph, layer=0):
        self._draw_stage_glyph(x, y, glyph, layer)

    def _draw_stage_glyph(self, x, y, glyph, layer=0):
        console = self._game.renderer.root_console
        console.layer(layer)
        console.color(glyph.fg)
        console.put(x, y, glyph.char)

    def render(self) -> None:
        self._game.renderer.clear()
        self.render_visible_tiles(self._game.area.current_area.grid)
        self.render_visible_entities()
        self.draw_debugging_overlay()

    def draw_debugging_overlay(self):
        console = self._game.renderer.root_console
        x = self._game.player.position[0]
        y = self._game.player.position[1]
        offset = STAGE_WIDTH + 4

        console.puts(offset, 4, "cell position")
        console.puts(offset, 5, "----------------")
        console.puts(offset, 6, "x: " + str(x))
        console.puts(offset + 8, 6, "y: " + str(y))

        console.puts(offset, 8, "coordinates")
        console.puts(offset, 9, "----------------")
        console.puts(offset, 10, "x: " + str(x // 2))
        console.puts(offset + 8, 10, "y: " + str(y))

        arr = self._game.area.current_area._tiles
        console.puts(offset, 14, "array w: " + str(arr.width))
        console.puts(offset, 15, "array h: " + str(arr.height))

    def update(self, dt) -> None:
        self.render()
