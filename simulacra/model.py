from __future__ import annotations
from typing import Dict, Tuple, List, Set, TYPE_CHECKING
from event_queue import EventQueue
from player import Player
from message import Message

from action import Impossible
from factories.factory_service import FactoryService
from managers.manager_service import ManagerService
from managers.result_manager import ResultManager
from result import Result

if TYPE_CHECKING:
    from component import Component
    from item import Item
    from entity import Entity
    from area import Area
    from actor import Actor


class AreaData(dict):

    current_area = None

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, area: Area) -> None:
        self.current_area = area
        self[area.area_model.NAME] = area

    def get_items(self):
        return self[self.current_area.area_model.NAME].items


class EntityData(dict):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, entity: Entity) -> None:
        for key, value in entity.components.items():
            self[entity.NAME] = {key: value}


class Model:

    def __init__(self) -> None:
        self.area_data = AreaData(self)
        self.entity_data = EntityData(self)
        self.scheduler = EventQueue()
        self.log: List[Message] = []
        self._effect_flag = False
        
    @property
    def effect_flag(self) -> bool:
        return self._effect_flag
    
    @effect_flag.setter
    def effect_flag(self, value: bool) -> None:
        if self._effect_flag != value:
            self._effect_flag = value            

    @property
    def player(self) -> Player:
        return self.area_data.current_area.player

    @property
    def area(self) -> Area:
        return self.area_data.current_area
    
    @property
    def actors(self) -> Set[Actor]:
        return self.area_data.current_area.actor_model.actors
    
    @property
    def nearby_items(self) -> List[List[Item]]:
        return self.area.nearby_items
    
    @property
    def container_items(self) -> List[Item]:
        pass
    
    def get_components_on_entity(self, entity: Entity) -> Dict[str, Component]:
        return entity.components
    
    def get_component_by_name(self, entity: Entity, name: str) -> Component:
        entity_components =  self.get_components_on_entity(entity)
        return entity_components[name.upper()]
    
    def get_all_components_by_name(self, name: str) -> Dict[str, Component]:
        pass

    def get_opts_from_components(
            self, 
            entity: Entity
        ) -> Tuple[List[Component], List[Dict]]:
        
        components = self.get_components_on_entity(entity)
        options = []
        for component in components.items():
            for option in component[1].options.items():
                options.append(option)
        return options

    def loop(self) -> None:
        frame_count = 0
        while True:
            frame_count += 1
            # This will count the frames between each screen update
            self.scheduler.invoke_next()
            
    def report(self, msg: str) -> None:
        print(msg)
        if self.log and self.log[-1].msg == msg:
            self.log[-1].count += 1
        else:
            self.log.append(Message(msg))
