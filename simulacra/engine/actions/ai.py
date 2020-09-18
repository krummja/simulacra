from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING, Optional

import numpy as np
import tcod.path

from simulacra.engine.actions import Action, Impossible
from simulacra.engine.actions import common
from simulacra.states.game import PlayerReady

if TYPE_CHECKING:
    from simulacra.engine.actor import Actor


class AI(Action):
    pass


class PlayerControl(AI):

    def act(self) -> None:
        event = self.actor.event
        while event is self.actor.event:
            next_action = PlayerReady(self.actor.location.area.model).loop()
            if next_action is None:
                continue
            try:
                # TODO: I have NO IDEA why this is misbehaving...
                next_action.plan().act()  # type: ignore
            except Impossible as exc:
                self.report(exc.args[0])