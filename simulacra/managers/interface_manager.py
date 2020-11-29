from __future__ import annotations
from typing import Dict, Set, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ui_primitives.element_base import ElementBase
    from panel import Panel
    from actor import Actor
    from area import Area
    from component import Component
    from entity import Entity
    from item import Item
    from location import Location
    from model import Model


# TODO: Do I need this class, as opposed to relying on my Model data structures?
class InterfaceManager:
    
    def __init__(self) -> None:
        self._model = None
        self._elements: Dict[str, ElementBase] = {}
        
    @property
    def model(self) -> Model:
        return self._model
    
    @model.setter
    def model(self, value: Model) -> None:
        self._model = value

    def get_element(self, element_name) -> ElementBase:
        return self._elements[element_name]

    def register_element(self, element: Panel) -> None:
        self._elements[element.NAME] = element
    
    def deregister_element(self, element_name: str) -> None:
        del self._elements[element_name]