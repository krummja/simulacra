from __future__ import annotations
from typing import List, TYPE_CHECKING
from event_queue import EventQueue
from player import Player
from message import Message
from factories.factory_service import FactoryService

if TYPE_CHECKING:
    from managers.game_context import GameContext
    from entity import Entity
    from area import Area


class AreaData(dict):

    current_area = None

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, area: Area) -> None:
        self.current_area = area
        self[area.area_model.ident] = area

    def get_items(self):
        return self[self.current_area.area_model.ident].items


class EntityData(dict):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, entity: Entity) -> None:
        for key, value in entity.components.items():
            self[entity.ident] = {key: value}


class Model:

    def __init__(self) -> None:
        self.context = None
        self.area_data = AreaData(self)
        self.entity_data = EntityData(self)
        self.scheduler = EventQueue()
        self.factory_service = FactoryService(self)
        self.log: List[Message] = []

    @property
    def player(self) -> Player:
        return self.area_data.current_area.player

    def loop(self) -> None:
        while True:
            self.scheduler.invoke_next()

    # TODO: This would be best as a separate UI element
    def report(self, msg: str) -> None:
        print(msg)
        if self.log and self.log[-1].msg == msg:
            self.log[-1].count += 1
        else:
            self.log.append(Message(msg))
