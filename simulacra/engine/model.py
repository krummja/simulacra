from __future__ import annotations
from typing import List

from engine.area import Area
from engine.event_queue import EventQueue
from engine.log import Message
from engine.player import Player


class Model:
    current_area: Area

    def __init__(self) -> None:
        self.log: List[Message] = []
        self.scheduler = EventQueue()

    @property
    def player(self) -> Player:
        return self.current_area.player

    def report(self, text: str) -> None:
        print(text)
        if self.log and self.log[-1].text == text:
            self.log[-1].count += 1
        else:
            self.log.append(Message(text))

    def loop(self) -> None:
        while True:
            self.scheduler.invoke_next()
