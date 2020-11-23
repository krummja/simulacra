from __future__ import annotations

from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.item_factory import ItemFactory


class FactoryService:

    def __init__(self) -> None:
        self.body_factory = None
        self.character_factory = None
        self.item_factory = None
