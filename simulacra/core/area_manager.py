from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from data.areas.test_area import TestArea

from simulacra.world.area import Area
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class AreaManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._current_area: Optional[Area] = None
        self._areas = {
            'TEST': TestArea(self)
            }
        self.set_area('TEST')

    @property
    def current_area(self) -> Optional[Area]:
        return self._current_area

    def set_area(self, area: str) -> None:
        self._current_area = self._areas[area]

    def create_tile_at_pos(self, x: int, y: int):
        tile = self._game.ecs.engine.create_entity()
        tile.add("TILE", {'move_cost': 0, 'transparent': True, 'char': ord('#'), 'color': (255,0,0), 'bg': (0,0,0)})
        self._current_area.tiles.tiles[y, x] = tile['TILE'].data

    def fill_area(self) -> None:
        tile = self._game.ecs.engine.create_entity()
        tile.add("TILE", {'move_cost': 0, 'transparent': True, 'char': ord('.'), 'color': (100, 100, 100), 'bg': (0,0,0)})
        self._current_area.tiles.tiles[:] = tile['TILE'].data
