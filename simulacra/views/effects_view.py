from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Type

from tcod import Console

import time
from random import uniform, randint
from math import sin, cos

from config import *
from view import View
from views.stage_view import StageView

from managers.effects_manager import EffectsManager
from particles.emitters import TestEffect

if TYPE_CHECKING:
    from states.effects_state import EffectsState
    from model import Model
    from state import State


class EffectsView(StageView):
    
    def __init__(self, state: EffectsState, model: Model) -> None:
        super().__init__(state, model)
        self.manager = EffectsManager(model)
        self.manager.add_effect(TestEffect(model.player.location.x,
                                           model.player.location.y,
                                           10,
                                           model.area))
        # self.p_system = self.state.p_system

    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        area = self.model.area_data.current_area
        self.manager.draw(consoles)
        
        if DEBUG:
            state_text = "EFFECTS STATE"
            width = len(state_text)
            consoles['ROOT'].print(
                (STAGE_PANEL_WIDTH - width) // 2, 1, state_text, (255, 0, 0))
