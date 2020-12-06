from __future__ import annotations  # type: ignore
from typing import Generic, Optional, TYPE_CHECKING

import time
import tcod

from graphic import Graphic
from state import State, T, StateBreak
from states.area_state import AreaState
from views.effects_view import EffectsView

if TYPE_CHECKING:
    from location import Location
    from model import Model
    from view import View


class Particle(Graphic):
    char = ord("*")
    color = (255, 0, 0)
    bg = (0, 0, 0)
    
    def __init__(self, location: Location) -> None:
        self.location = location


class EffectsState(AreaState[None]):
    
    NAME = "Effects"
    
    def __init__(self, model: Model) -> None:
        super().__init__(model)
        self._view = EffectsView(self, model)
        self.manager = self.manager_service.animation_manager
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        """We want to disable input for the duration of an effect animation."""
        
        if event.sym == tcod.event.K_ESCAPE:
            self.cmd_quit()
            
        if event.sym == tcod.event.K_F1:
            self.cmd_admin1()
            
        if event.sym == tcod.event.K_F2:
            self.cmd_admin2()

    def cmd_admin1(self):
        print("ADMIN >> Starting Animation Loop")
        self.manager.running = True

    def cmd_admin2(self):
        print("ADMIN >> Injecting static particle")
        player_x = self.model.player.location.x
        player_y = self.model.player.location.y
        particle = Particle(self.model.area[player_y + 2, player_x + 2])
        try:
            self.model.area_data.current_area.particle_model.particles[
                player_x + 2, player_y + 2
            ].append(particle)
        except KeyError:
            print("Particle injected")
            self.model.area_data.current_area.particle_model.particles[
                player_x + 2, player_y + 2
            ] = [particle]

    def cmd_quit(self):
        raise StateBreak()