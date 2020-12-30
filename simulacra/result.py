from __future__ import annotations  # type: ignore

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from action import Action
    from actor import Actor
    from message import Message


class Result:

    uid: int = 0

    def __init__(
            self,
            actor: Actor,
            event: Action,
            done: bool = False,
            success: bool = False,
            effect = None,
            message: Optional[Message] = None
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
