"""ENGINE.EVENTS.Player_Control"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from engine.states.player_ready_state import PlayerReadyState

from .action import Action, Impossible
from .control import Control
from .result import Result

if TYPE_CHECKING:
    from engine.states.state import State


class PlayerControl(Control):
    """Controller class for the player character."""
    # pylint: disable=no-member

    def act(self) -> Result:
        player_state: State = PlayerReadyState(self.model)
        event = self.actor.event
        while event is self.actor.event:
            next_action: Optional[Action] = player_state.loop()
            if next_action is None:
                continue
            try:
                success = next_action.plan().act()
                result: Result = self.make_result(success)
                player_state.managers['results'].add_result(result)
            except Impossible as failure:
                failure = failure.args[0]
                result = self.make_result(failure)
                player_state.managers['results'].add_result(result)
