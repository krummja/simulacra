from __future__ import annotations
from typing import List, TYPE_CHECKING
from event_queue import EventQueue
from player import Player
from message import Message


class AreaData(dict):

    current_area = None

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, area):
        self.current_area = area
        self[f'{area.ident}'] = area

    def get_items(self):
        return self[f'{self.current_area.ident}'].items


class EntityData(dict):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def register(self, entity) -> None:
        self[f'{entity.ident}'] = entity
        for component in entity.components:
            self[f'{entity.ident}'][f'{component.ident}'] = component.data


class Model:

    def __init__(self) -> None:
        self.area_data = AreaData(self)
        self.entity_data = EntityData(self)
        self.scheduler = EventQueue()
        self.log: List[Message] = []

    @property
    def player(self) -> Player:
        return self.area_data.current_area.player

    def loop(self) -> None:
        while True:
            self.scheduler.invoke_next()

    def report(self, msg: str) -> None:
        print(msg)
        if self.log and self.log[-1].msg == msg:
            self.log[-1].count += 1
        else:
            self.log.append(Message(msg))
