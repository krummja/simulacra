from __future__ import annotations
from typing import TYPE_CHECKING

from engine.actions import Action

if TYPE_CHECKING:
    from engine.components.actor import Actor


class Behavior(Action):

    def __init__(self: Behavior, actor: Actor) -> None:
        super().__init__(actor)
        self.actor = actor
