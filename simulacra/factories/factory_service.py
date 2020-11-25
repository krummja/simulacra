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
        self.interface_factory = InterfaceFactory() 
        self.body_factory = None
        self.character_factory = None
        self.item_factory = None
