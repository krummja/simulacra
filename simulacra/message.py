from __future__ import annotations
from typing import TYPE_CHECKING


class Noun:
    pass


class Message:

    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.count = 1

    def __str__(self) -> str:
        if self.count > 1:
            return f"{self.msg} (x{self.count})"
        return self.msg
