from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from states.effects_state import EffectsState
from action import Action, Impossible
from result import Result
from control import Control
from states.player_ready_state import PlayerReadyState

from managers.manager_service import ManagerService


class PlayerControl(Control):

    def act(self) -> Result:
        event = self.actor.event
        while event is self.actor.event:
            next_action: Optional[Action] = PlayerReadyState(self.model).loop()
            if next_action is None:
                continue
            try:
                success = next_action.plan().act()
                self.make_result(success)
            except Impossible as failure:
                failure = failure.args[0]
                self.make_result(failure)
