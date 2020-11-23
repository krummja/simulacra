from __future__ import annotations
from typing import TYPE_CHECKING

from action import Action, Impossible
from control import Control
from states.player_ready_state import PlayerReadyState


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
