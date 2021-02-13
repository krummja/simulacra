from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from collections import defaultdict

from .system import System
from simulacra.core.options import *
from simulacra.utils.render_utils import *

if TYPE_CHECKING:
    from simulacra.core.game import Game
    from simulacra.ecs.components.renderable import Renderable


class RenderSystem(System):
    x_offset = ((CONSOLE_WIDTH - STAGE_PANEL_WIDTH) // 2)
    y_offset = 1

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.console = self.game.renderer.root_console
        self.area_grid = self.game.world.current_area.grid

        self._query = self.ecs.create_query(
            all_of=[
                'Renderable',
                'Sprite'
                ])

    def render_tile(self, x: int, y: int) -> None:
        world = self.game.camera.screen_to_world(x, y)

        if not self.game.camera.is_in_view(world['x'], world['y']):
            return

        x, y = tile_from_subtile(*subtile_from_cell(x, y))
        position = self.x_offset + x, self.y_offset + y

        if self.area_grid.visible[world['x'], world['y']]:
            self.draw_visible(wx=world['x'], wy=world['y'], at=position)
        elif self.area_grid.explored[world['x'], world['y']]:
            self.draw_explored(wx=world['x'], wy=world['y'], at=position)
        else:
            self.draw_unknown(wx=world['x'], wy=world['y'], at=position)

    def draw_visible(self, *, wx: int, wy: int, at: Tuple[int, int]) -> None:
        renderable = self.area_grid.tiles[wx][wy].entity['Renderable'].char
        self.console.layer(self.game.renderer.layers['GROUND'])
        self.console.color(0xFFFFFFFF)
        self.console.put(*at, renderable)

    def draw_explored(self, *, wx: int, wy: int, at: Tuple[int, int]) -> None:
        renderable = self.area_grid.tiles[wx][wy].entity['Renderable'].variant
        self.console.layer(self.game.renderer.layers['GROUND'])
        self.console.color(0x88FFFFFF)
        self.console.put(*at, renderable)

    def draw_unknown(self, *, wx: int, wy: int, at: Tuple[int, int]) -> None:
        explored = self.game.world.current_area.grid.explored
        top_left = explored[wx - 1][wy - 1]
        top = explored[wx][wy - 1]
        left = explored[wx - 1][wy]

        tile = {
            (True,  True,  True ): 'unknown2',
            (True,  True,  False): 'unknown3',
            (True,  False, True ): 'unknown4',
            (True,  False, False): 'unknown5',
            (False, True,  True ): 'unknown8',
            (False, True,  False): 'unknown6',
            (False, False, True ): 'unknown7',
            (False, False, False): 'unknown1',
            }
        selection = tile[(top_left, top, left)]

        self.console.layer(self.game.renderer.layers['UNKNOWN'])
        self.console.color(0xFFFFFFFF)
        self.console.put(*at, self.game.renderer.sprites.get_codepoint('other', selection))

    def render_entity(self, x: int, y: int) -> None:
        entities = defaultdict(list)
        world = self.game.camera.screen_to_world(x, y)
        if not self.game.camera.is_in_view(world['x'], world['y']):
            return

        for entity in self._query.result:
            entities[entity['POSITION'].xy].append(entity['Renderable'])

        if entities[world['x'], world['y']]:
            graphic = min(entities[world['x'], world['y']])
            self.console.layer(self.game.renderer.layers['ENTITY BASE'])
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

    def alpha_subtract(self, alpha: int, value: int, shift: int) -> int:
        return int(((alpha >> shift) - value) << shift)
