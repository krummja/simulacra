from __future__ import annotations

from engine.actions.behaviors import Behavior
from engine.actions import Impossible
from states.in_game import PlayerReady


class PlayerControl(Behavior):

    def act(self: PlayerControl) -> None:
        event = self.actor.event
        while event is self.actor.event:
            next_action = PlayerReady(self.actor.location.area.model).loop()
            if next_action is None:
                continue
            try:
                next_action.plan().act()
            except Impossible as exc:
                self.report(exc.args[0])
