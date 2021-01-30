from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from data.areas.test_area import TestArea

from simulacra.world.area import Area
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class AreaManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
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
