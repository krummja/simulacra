from __future__ import annotations
from typing import Dict, List, Tuple, TYPE_CHECKING
from collections import defaultdict

from simulacra.utils.debug import debugmethods

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

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION'    ],
            none_of=[ 'INVISIBLE'   ])

    def render_visible_entities(self, tile_grid: TileGrid) -> None:
        console = self._game.renderer.root_console
        cam_x, cam_y = self.game.camera.position

        # Set up our visible entities dict
        visible_entities: Dict[Tuple[int, int], List[Entity]] = defaultdict(list)

        # Grab all of our RENDERABLE entities with a POSITION
        for entity in self._query.result:
            e_x, e_y = entity['POSITION'].x - cam_x, entity['POSITION'].y - cam_y

            # If they're outside the stage panel, don't render
            if not (0 <= e_x < STAGE_PANEL_WIDTH and
                    0 <= e_y < STAGE_PANEL_HEIGHT):
                continue

            # If they're not visible, don't render
            if not tile_grid.visible[entity['POSITION'].ij]:
                continue

            # Override the background color of the entity to match the tile beneath
            entity['RENDERABLE'].bg = self.get_bg_color(e_x, e_y)

            # Generate the visible entity list for each dict position
            visible_entities[e_y, e_x].append(entity['RENDERABLE'])

        # Get the ij indexed position and the graphics data
        for ij, graphics in visible_entities.items():
            g = min(graphics)

            # Push the graphics data to the console
            console.tiles_rgb[["ch", "fg", "bg"]][ij] = g.char, g.color, g.bg

    def render_visible_tiles(self, tile_grid: TileGrid) -> None:
        console = self._game.renderer.root_console
        screen_view, _ = self._game.camera.viewport
        console.tiles_rgb[screen_view] = self._game.renderer.select_tile_mask(tile_grid)

    def get_bg_color(self, x: int, y: int) -> List[int]:
        cam_x, cam_y = self._game.camera.position
        target_x, target_y = x + cam_x, y + cam_y
        target_tile = self._game.area.current_area.grid.tiles[target_y, target_x]
        return list(target_tile[2][2][0:3])

    def update_camera_position(self) -> None:
        self._game.camera.position = self._game.player.entity['POSITION'].xy

    def render(self) -> None:
        self._game.renderer.clear()
        self.update_camera_position()
        self.render_visible_tiles(self._game.area.current_area.grid)
        self.render_visible_entities(self._game.area.current_area.grid)

    def update(self, dt) -> None:
        self.render()
