from __future__ import annotations  # type: ignore
from typing import List, TYPE_CHECKING


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

    def __init__(self) -> None:
        self.log: List[Message] = []

    @property
    def player(self):
        pass

    def report(self, text: str) -> None:
        pass

    def loop(self) -> None:
        while True:
            pass