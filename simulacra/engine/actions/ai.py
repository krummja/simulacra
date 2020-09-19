from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING, Optional

import numpy as np
import tcod.path

from engine.actions import Action, common, Impossible
from states.game import PlayerReady

if TYPE_CHECKING:
    from engine.actor import Actor


class AI(Action):
    pass


class PlayerControl(AI):

    def act(self) -> None:
        event = self.actor.event
        while event is self.actor.event:
            next_action = PlayerReady(self.actor.location.area.model).loop()
            # print("Debug in engine.actions.ai.PlayerControl")
            # print(next_action)
            if next_action is None:
                continue
            try:
                next_action.plan().act()
            except Impossible as exc:
                self.report(exc.args[0])