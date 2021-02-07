from __future__ import annotations
from typing import TYPE_CHECKING

from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class WorldManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.areas = {}

        for area in self.game.area._areas:
            self.areas[area] = {}

    @property
    def current_area_data(self):
        return self.areas[self.game.area.current_area.name]

    def generate_world(self):
        pass

    def generate_area(self):
        pass
