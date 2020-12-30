from __future__ import annotations

from typing import TYPE_CHECKING

from action import Action

if TYPE_CHECKING:
    from actor import Actor


class Control(Action):

    def __init__(self, actor: Actor) -> None:
        super().__init__(actor)

    def plan(self) -> Action:
        return self
