from __future__ import annotations  # type: ignore
from typing import Any, Dict, TYPE_CHECKING

from message import Message


class Result:
    
    uid: int = 0
    
    def __init__(
            self,
            actor,
            event,
            done = False,
            success = False,
            effect = None,
            message = None
        ) -> None:
        self.actor = actor
        self.event = event
        self.done = done
        self.success = success
        self.effect = effect
        self.message = message
                
    def __lt__(self, other: Result) -> bool:
        return self.uid < other.uid
    
    def __str__(self) -> str:
        return f"{self.uid}\n{self.actor}\n{self.event}\n{self.success}\n{self.message}"