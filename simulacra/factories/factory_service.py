from __future__ import annotations
from typing import TYPE_CHECKING

from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.item_factory import ItemFactory
from factories.interface_factory import InterfaceFactory

if TYPE_CHECKING:
    from model import Model


class FactoryService:

    def __init__(self) -> None:
        self._model: Model = None
        self.interface_factory = InterfaceFactory() 
        self.body_factory = BodyFactory()
        self.character_factory = CharacterFactory()
        self.item_factory = ItemFactory()
    
    @property
    def model(self) -> Model:
        return self._model
    
    @model.setter
    def model(self, value: Model) -> None:
        self._model = value
        self.body_factory.model = value
        self.character_factory.model = value
        self.item_factory.model = value