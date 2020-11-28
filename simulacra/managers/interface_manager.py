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
        
    @property
    def model(self) -> Model:
        return self._model
    
    @model.setter
    def model(self, value: Model) -> None:
        self._model = value

    def area(self) -> Area:
        return self.model.area_data.current_area
    
    def actors(self) -> Set[Actor]:
        return self.model.area_data.current_area.actor_model.actors
    
    def nearby_items(self) -> List[List[Item]]:
        area = self.area()
        area.item_model.get_nearby()
        return area.nearby_items
    
    def container_items(self, x: int, y: int) -> List[Item]:
        area = self.area()
        try:
            if area.items[y, x][0].components['PHYSICS'].size == 'large':
                container = self.area.items[y, x][0]
                if container.components['INVENTORY']:
                    return container.components['INVENTORY'].contents
        except KeyError:
            pass
    
    def components_on_entity(self, entity: Entity) -> Dict[str, Component]:
        return entity.components
    
    def component_by_name(self, entity: Entity, name: str) -> Dict[str, Component]:
        return self.components_on_entity(name)
    
    def all_components_by_name(self, name: str):
        pass