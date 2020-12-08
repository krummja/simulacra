from __future__ import annotations  # type: ignore
from typing import Generic, Optional, Tuple, TYPE_CHECKING

import random
import time
import tcod

from config import *

from graphic import Graphic
from state import State, T, StateBreak
from states.player_ready_state import PlayerReadyState
from views.effects_view import EffectsView
from particles.particle_system import ParticleSystem

if TYPE_CHECKING:
    from location import Location
    from model import Model
    from view import View


class EffectsState(PlayerReadyState[None]):
    
    NAME = "Effects"
    
    def __init__(
            self, 
            model: Model,
            effect = None
        ) -> None:
        super().__init__(model)
        self._time = 0
        self.effect = effect
        self.manager = self.manager_service.animation_manager
        self.p_system = ParticleSystem(
            self.model,
            self.model.player.location.x,
            self.model.player.location.y)
        self._view = EffectsView(self, model)
        
    def loop(self):
        time.sleep(5)
        raise StateBreak()
        
    def cmd_admin1(self):
        print("ADMIN >> Starting Animation Loop")
        self.manager.running = True

    def cmd_quit(self):
        raise StateBreak()