from __future__ import annotations
from typing import TYPE_CHECKING

from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.item_factory import ItemFactory

if TYPE_CHECKING:
    from model import Model


class FactoryService:

    def __init__(self, model: Model) -> None:
        self.body_factory = BodyFactory(model, self)
        self.character_factory = CharacterFactory(model, self)
        self.item_factory = ItemFactory(model, self)
