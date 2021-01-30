from __future__ import annotations
from typing import TYPE_CHECKING
from collections import defaultdict

from numpy.lib.arraysetops import isin

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
        tile = self._game.area.current_area.grid.ground[world['x'], world['y']]['TILE']
        console.layer(0)
        console.color(tile.fg)
        x, y = tile_from_subtile(*subtile_from_cell(x, y))
        console.put(x, y, tile.char)

    def render_obstacle(self, x, y):
        world = self._game.camera.screen_to_world(x, y)
        if not self._game.camera.is_in_view(world['x'], world['y']):
            return
        if isinstance(self._game.area.current_area.grid.obstacle[world['x'], world['y']], int):
            return
        console = self._game.renderer.root_console
        tile = self._game.area.current_area.grid.obstacle[world['x'], world['y']]['TILE']
        console.layer(1)
        console.color(tile.fg)
        x, y = tile_from_subtile(*subtile_from_cell(x, y))
        console.put(x, y, tile.char)

    def render(self) -> None:
        self._game.renderer.clear()
        for x in range(self._game.camera.width):
            for y in range(self._game.camera.height):
                self.render_tile(x, y)
                self.render_entity(x, y)
                self.render_obstacle(x, y)
        self.draw_ui_frames()

    def draw_ui_frames(self) -> None:
        self._game.renderer.root_console.layer(5)

        # Stage Panel
        self._game.renderer.root_console.put(   0,  0, 0xEF04 + (16*0) )
        self._game.renderer.root_console.put( 124,  0, 0xEF06 + (16*0) )
        self._game.renderer.root_console.put(   0, 42, 0xEF04 + (16*2) )
        self._game.renderer.root_console.put( 124, 42, 0xEF06 + (16*2) )
        for x in range(0, 124, 2):
            self._game.renderer.root_console.put( 2+x, 0,  0xEF05 + (16*0) )
            self._game.renderer.root_console.put( 2+x, 42, 0xEF05 + (16*2) )
        for y in range(0, 40, 2):
            self._game.renderer.root_console.put( 0,   2+y, 0xEF04 + (16*1) )
            self._game.renderer.root_console.put( 124, 2+y, 0xEF06 + (16*1) )

        # Log Panel
        self._game.renderer.root_console.put( 1,   44, 0xEF00 + (16*0) )
        self._game.renderer.root_console.put( 102, 44, 0xEF02 + (16*0) )
        self._game.renderer.root_console.put( 1,   54, 0xEF00 + (16*2) )
        self._game.renderer.root_console.put( 102, 54, 0xEF02 + (16*2) )
        for x in range(0, 100, 4):
            self._game.renderer.root_console.put( 3+x, 44, 0xEF01 + (16*0) )
            self._game.renderer.root_console.put( 3+x, 54, 0xEF01 + (16*2) )
            for y in range(0, 8, 2):
                self._game.renderer.root_console.put( 3+x, 46+y, 0xEF01 + (16*1) )
        for y in range(0, 8, 2):
            self._game.renderer.root_console.put( 1,   46+y, 0xEF00 + (16*1) )
            self._game.renderer.root_console.put( 102, 46+y, 0xEF02 + (16*1) )

        self._game.renderer.root_console.layer(6)
        self._game.renderer.root_console.color(0xFF000000)
        self._game.renderer.root_console.puts(3, 45, "[font=ui]Hello! This is a test of the log panel. :)[/font]")
        self._game.renderer.root_console.puts(3, 46, "[font=ui]This is all static text at the moment... :([/font]")
        self._game.renderer.root_console.puts(3, 48, "[font=ui]But! It supports [color=red]c[/color][color=purple]o[/color][color=green]l[/color][color=orange]o[/color][color=blue]r[/color][color=white]s[/color]![/font]")
        self._game.renderer.root_console.puts(3, 52, "[font=big]and BIG text! :D[/font]")


    def update(self, dt) -> None:
        self.render()

