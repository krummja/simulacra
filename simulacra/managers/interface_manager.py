"""
The Interface Manager allows for the abstraction of certain functions important
to GUI setup, teardown, rendering, data management, and state transfer.
"""

from __future__ import annotations
from typing import Dict, Set, List, TYPE_CHECKING

if TYPE_CHECKING:
    from actor import Actor
    from area import Area
    from component import Component
    from entity import Entity
    from item import Item
    from location import Location
    from model import Model


class InterfaceManager:
    
    def __init__(self) -> None:
        self._model = None
        self._elements = {}
        
    @property
    def model(self) -> Model:
        return self._model
    
    @model.setter
    def model(self, value: Model) -> None:
        self._model = value

    def register_element(self, element) -> None:
        self._elements[element.NAME] = element
    
    def deregister_element(self, element_name: str) -> None:
        del self._elements[element_name]
