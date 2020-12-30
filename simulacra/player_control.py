from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from action import Action, Impossible
from control import Control
from result import Result
from states.player_ready_state import PlayerReadyState


class PlayerControl(Control):

    def act(self) -> Result:
        player_state = PlayerReadyState(self.model)
        event = self.actor.event
        while event is self.actor.event:
            next_action: Optional[Action] = player_state.loop()
            if next_action is None:
                continue
            try:
                # TODO: Does this actually return anything?
                success = next_action.plan().act()
                result: Result = self.make_result(success)
                player_state.manager_service.result_manager.add_result(result)
            except Impossible as failure:
                failure = failure.args[0]
                result = self.make_result(failure)
                player_state.manager_service.result_manager.add_result(result)
