from __future__ import annotations  # type: ignore
from typing import Generic, Optional, Tuple, TYPE_CHECKING

import random
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


max_particle_moves = 10

class Particle(Graphic):
    char = ord("*")
    color = (0, 0, 0)
    bg = (0, 0, 0)
    distance = 0
    
    def __init__(self, system, location: Location, vx, vy, color) -> None:
        self.system = system
        self.x = location.x
        self.y = location.y
        self.vx = vx
        self.vy = vy
        self.color = color
    
    def is_dead(self):
        if self.distance > max_particle_moves:
            return True
        else:
            return False
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.distance += 1
        
    def draw(self, consoles):
        cam_x, cam_y = self.system.model.area.camera.get_camera_pos()
        consoles['EFFECTS'].clear()
        consoles['EFFECTS'].print( 
            x=self.x - cam_x, 
            y=self.y - cam_y,
            string="*",
            fg=self.color)
        
        consoles['EFFECTS'].blit(
            consoles['ROOT'],
            0, 0, 0, 0,
            fg_alpha=1.0,
            bg_alpha=0.0)
        

class ParticleSystem:
    
    def __init__(self, model: Model, x, y):
        self.model = model
        self.origin = x, y
        self.particles = []
    
    def update(self):
        x, y = self.origin
        for p in self.particles:
            p.move()
            if p.is_dead():
                self.particles.remove(p)
    
    def add_particles(self, number, x, y):
        for i in range(0, number):
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            vx = x
            vy = y
            p = Particle(self, self.model.area[self.origin[0], self.origin[1]], vx, vy, (r, g, b))
            self.particles.append(p)
    
    def draw(self, consoles):
        cam_x, cam_y = self.model.area.camera.get_camera_pos()
        for p in self.particles:
            p.draw(consoles)
        

class EffectsState(AreaState[None]):
    
    NAME = "Effects"
    
    def __init__(self, model: Model) -> None:
        super().__init__(model)
        self._view = EffectsView(self, model)
        self._time = 0
        self.manager = self.manager_service.animation_manager
        self.p_system = ParticleSystem(
            self.model,
            self.model.player.location.x,
            self.model.player.location.y)
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        """We want to disable input for the duration of an effect animation."""
        
        if event.sym == tcod.event.K_ESCAPE:
            self.cmd_quit()
        if event.sym == tcod.event.K_F1:
            self.cmd_admin1()
        if event.sym in self.MOVE_KEYS:
            dx = self.MOVE_KEYS[event.sym][0]
            dy = self.MOVE_KEYS[event.sym][1]
            self.p_system.add_particles(1, dx, dy)

    def cmd_admin1(self):
        print("ADMIN >> Starting Animation Loop")
        self.manager.running = True

    def cmd_quit(self):
        raise StateBreak()