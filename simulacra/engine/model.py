"""ENGINE.Model"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

from engine.events import EventQueue
from engine.entities import Player

if TYPE_CHECKING:
    from engine.events import Actor, Message
    from engine.areas import Area
    from engine.entities.entity import Entity


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
    """Carries references to all of the data that should be persistent
    for a given session.

    The Model is also responsible for initializing the `EventQueue` and
    starting the scheduling loop. Finally, it is the mediator for
    communication between the game logic and log reporting."""

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
