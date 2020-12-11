from __future__ import annotations  # type: ignore
from typing import Generic, Optional, Tuple, TYPE_CHECKING

import random
import time
import tcod

from config import *

from graphic import Graphic
from state import State, T, StateBreak, EffectsBreak
from states.area_state import AreaState
from views.effects_view import EffectsView
from particles.particle_system import ParticleSystem

if TYPE_CHECKING:
    from location import Location
    from model import Model
    from view import View


class EffectsState(AreaState[None]):
    
    NAME = "Effects"
    
    def __init__(
            self, 
            model: Model,
            effect = None
        ) -> None:
        super().__init__(model)
        self.effect = effect
        self.p_system = ParticleSystem(
            self.model,
            self.model.player.location.x,
            self.model.player.location.y)
        self._view = EffectsView(self, model)
        self.model.effect_flag = True
        self.animation_loop()
    
    def animation_loop(self):
        if self.effect:
            self.effect(self.p_system).fire()
        else:
            raise EffectsBreak()
    
    def cmd_quit(self):
        raise EffectsBreak()