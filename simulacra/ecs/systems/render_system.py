from __future__ import annotations
from typing import Dict, List, Tuple, TYPE_CHECKING
from collections import defaultdict

import numpy as np

from simulacra.utils.geometry import Rect

from simulacra.utils.render_utils import argb_from_color
from simulacra.core.rendering.tile_data import tile_graphic

from .system import System
from simulacra.core.options import *

if TYPE_CHECKING:
    from tcod.console import Console
    from ecstremity import Entity
    from simulacra.core.game import Game
    from simulacra.core.rendering.tile_grid import TileGrid


class RenderSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.camera_bounds = None
        self.render_offset = {'x': 0, 'y': 0}

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE'   ])

    # def render_visible_entities(self, tile_grid: TileGrid) -> None:
    #     console = self._game.renderer.root_console
    #     cam_x, cam_y = self.game.camera.position

    #     # Set up our visible entities dict
    #     visible_entities: Dict[Tuple[int, int], List[Entity]] = defaultdict(list)

    #     # Grab all of our RENDERABLE entities with a POSITION
    #     for entity in self._query.result:
    #         e_x, e_y = entity['POSITION'].x - cam_x, entity['POSITION'].y - cam_y

    #         # If they're outside the stage panel, don't render
    #         if not (0 <= e_x < STAGE_PANEL_WIDTH and
    #                 0 <= e_y < STAGE_PANEL_HEIGHT):
    #             continue

    #         # If they're not visible, don't render
    #         if not tile_grid.visible[entity['POSITION'].xy]:
    #             continue

    #         # Generate the visible entity list for each dict position
    #         visible_entities[e_x, e_y].append(entity['RENDERABLE'])

    #     # Get the ij indexed position and the graphics data
    #     for (x, y), graphics in visible_entities.items():
    #         g = min(graphics)

    #         # Push the graphics data to the console
    #         self.draw_tile(x, y, g, layer=1)

    def render_visible_entities(self, tile_grid):
        entities = defaultdict(list)
        for entity in self._query.result:
            if not (0 <= entity['POSITION'].x < CONSOLE_WIDTH and
                    0 <= entity['POSITION'].y < CONSOLE_HEIGHT):
                continue
            entities[entity['POSITION'].x, entity['POSITION'].y].append(entity['RENDERABLE'])

        for (x, y), graphics in entities.items():
            g = min(graphics)
            self.draw_tile(x, y, g, layer=1)

    def render_visible_tiles(self, tile_grid: TileGrid) -> None:
        for x in range(STAGE_WIDTH):
            for y in range(STAGE_HEIGHT):
                tile = tile_grid[x, y]['TILE']
                self.draw_tile(x, y, tile, layer=0)

    # def render_visible_tiles(self, tile_grid: TileGrid) -> None:
    #     self.position_camera(tile_grid)
    #     for x in range(self.camera_bounds.width):
    #         for y in range(self.camera_bounds.height):
    #             tile = tile_grid[x, y]['TILE'].char
    #             self.draw_tile(x, y, tile)

    def position_camera(self, tile_grid):
        range_width = max(0, tile_grid.width - STAGE_PANEL_WIDTH)
        range_height = max(0, tile_grid.height - STAGE_PANEL_HEIGHT)
        camera_range = Rect.from_edges(left=0, top=0, right=range_width, bottom=range_height)

        camera = (
            self._game.player.position[0] - (STAGE_PANEL_WIDTH // 2),
            self._game.player.position[1] - (STAGE_PANEL_HEIGHT // 2)
            )

        camera = camera_range.clamp(camera[0], camera[1])

        self.camera_bounds = Rect.from_edges(
            left=camera[0],
            top=camera[1],
            right=min(STAGE_PANEL_WIDTH, tile_grid.width),
            bottom=min(STAGE_PANEL_HEIGHT, tile_grid.height)
            )

        self.render_offset = {
            'x': max(0, STAGE_PANEL_WIDTH - tile_grid.width) // 2,
            'y': max(0, STAGE_PANEL_HEIGHT - tile_grid.height) // 2
            }

    def draw_tile(self, x, y, tile, layer=0):
        console = self._game.renderer.root_console
        console.layer(layer)
        console.color(tile.fg)
        console.put(x, y, tile.char)

    def update_camera_position(self) -> None:
        self._game.camera.position = self._game.player.entity['POSITION'].xy

    def render(self) -> None:
        self._game.renderer.clear()
        self.update_camera_position()
        self.render_visible_tiles(self._game.area.current_area.grid)
        self.render_visible_entities(self._game.area.current_area.grid)

    def update(self, dt) -> None:
        self.render()
