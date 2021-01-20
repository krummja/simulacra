from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from simulacra.world.area import Area
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class AreaManager(Manager):

    def __init__(self, game: Game) -> None:
        self.game = game
        self._current_area: Optional[Area] = None

    @property
    def current_area(self) -> Optional[Area]:
        return self._current_area
