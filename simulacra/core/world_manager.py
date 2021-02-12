from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.data.areas.unnamed_area import UnnamedArea
from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class WorldManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._current_area = None
        self.regions = {}
        self.areas = {
            'Unnamed Area': UnnamedArea
            }
        self.current_area = 'Unnamed Area'

    @property
    def current_area(self):
        return self._current_area

    @current_area.setter
    def current_area(self, area_name: str):
        self._current_area = self.areas[area_name](self)

    def generate_world(self):
        """Create and initialize a world consisting of many Area instances."""
        pass

    def generate_area(self):
        """Create and initialize a specific area using an Architect."""
        pass
