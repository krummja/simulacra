from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from action import Action, Impossible
from result import Result
from control import Control
from states.player_ready_state import PlayerReadyState
from managers.manager_service import ManagerService


class PlayerControl(Control):

    def act(self) -> Result:
        player_state = PlayerReadyState(self.model)
        event = self.actor.event
        while event is self.actor.event:
            next_action: Optional[Action] = player_state.loop()
            if next_action is None:
                continue
            try:
                success = next_action.plan().act()
                result = self.make_result(success)
                player_state.result_manager.add_result(result)
            except Impossible as failure:
                failure = failure.args[0]
                result = self.make_result(failure)
                player_state.result_manager.add_result(result)
