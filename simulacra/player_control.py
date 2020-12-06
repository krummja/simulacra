from __future__ import annotations
from typing import TYPE_CHECKING

from action import Result
from states.effects_state import EffectsState
from action import Action, Impossible
from control import Control
from states.player_ready_state import PlayerReadyState

from managers.manager_service import ManagerService


class PlayerControl(Control):

    result_manager = ManagerService().result_manager

    def act(self) -> None:
        event = self.actor.event
        while event is self.actor.event:
            next_action: Action = PlayerReadyState(
                self.actor.owner.location.area.model
                ).loop()
            if next_action is None:
                continue
            try:
                result = next_action.plan().act()
                # TODO: Find a place where the ResultManager can comfortably sit and observe
                self.result_manager.add_result(result)
            except Impossible as exc:
                self.report(exc.args[0])
