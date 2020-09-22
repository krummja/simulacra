from __future__ import annotations  # type: ignore
from typing import List, TYPE_CHECKING

from engine.queue import EventQueue

if TYPE_CHECKING:
    from engine.paths.player import Player
    from engine.area import Area


class Message:
    def __init__(self, text: str) -> None:
        self.text = text
        self.count = 1

    def __str__(self) -> str:
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text


class Model:
    """The model contains everything from a session which should be saved."""

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