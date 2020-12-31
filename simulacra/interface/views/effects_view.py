from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Type

from tcod import Console

from config import *
from .view import View
from .stage_view import StageView

from engine.particles.emitters import TestEffect

if TYPE_CHECKING:
    from engine.states.effects_state import EffectsState
    from engine.states.state import State
    from engine.model import Model


class EffectsView(StageView):

    def __init__(self, state: EffectsState, model: Model) -> None:
        super().__init__(state, model)
        self.manager = self.state.effects_manager
        self.manager.add_effect(TestEffect(model.player.location.x,
                                           model.player.location.y,
                                           10,
                                           model.area))

    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        area = self.model.area_data.current_area
        self.manager.draw(consoles)
