from __future__ import annotations
from typing import TYPE_CHECKING

from states.player_ready_state import PlayerReadyState
from action import Action, Impossible

if TYPE_CHECKING:
    from actor import Actor


class Control(Action):

    def __init__(self, actor: Actor) -> None:
        super().__init__(actor)

    def plan(self) -> Action:
        return self


class PlayerControl(Control):

    def act(self) -> None:
        event = self.actor.event
        while event is self.actor.event:
            next_action: Action = PlayerReadyState(
                self.actor.owner.location.area.model
                ).loop()
            if next_action is None:
                continue
            try:
                next_action.plan().act()
            except Impossible as exc:
                self.report(exc.args[0])
