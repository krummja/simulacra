from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

from event_queue import EventQueue
from message import Message
from player import Player

if TYPE_CHECKING:
    from actor import Actor
    from area import Area
    from component import Component
    from entity import Entity
    from item import Item


class AreaData(dict):

    current_area = None

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, area: Area) -> None:
        self.current_area = area
        self[area.area_model.uid] = area

    def get_items(self):
        return self[self.current_area.area_model.uid].items


class EntityData(dict):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, entity: Entity) -> None:
        for key, value in entity.components.items():
            self[entity.uid] = {key: value}


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

    def loop(self) -> None:
        while True:
            self.scheduler.invoke_next()

    def report(self, msg: Message) -> None:
        print(msg.text)
        if self.log and self.log[-1].text == msg.text:
            self.log[-1].count += 1
        else:
            self.log.append(msg)
