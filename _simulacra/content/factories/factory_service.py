from __future__ import annotations
from typing import TYPE_CHECKING

from content.factories.body_factory import BodyFactory
from content.factories.character_factory import CharacterFactory
from content.factories.item_factory import ItemFactory
from content.factories.tile_factory import TileFactory

from engine.util import Singleton

if TYPE_CHECKING:
    from engine.model import Model


class FactoryService(metaclass=Singleton):

    def __init__(self) -> None:
        self._model: Model = None
        self.body_factory = BodyFactory()
        self.character_factory = CharacterFactory()
        self.item_factory = ItemFactory()
        self.tile_factory = TileFactory()

    @property
    def model(self) -> Model:
        return self._model

    @model.setter
    def model(self, value: Model) -> None:
        self._model = value
        self.body_factory.model = value
        self.character_factory.model = value
        self.item_factory.model = value
        self.tile_factory.model = value
