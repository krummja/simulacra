from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

import random
from copy import copy

import tcod
import time

from graphic import Graphic
from particles.effect import Effect

if TYPE_CHECKING:
    from area import AreaLocation
    from particles.particle_system import ParticleSystem
    from tcod.console import Console


class Particle(Graphic):
    """A single particle in a Particle Effect."""
    
    char = "*"
    color = (255, 255, 255)
    bg = (0, 0, 0)
    distance = 0

    def __init__(
            self,
            chars: str,
            x: int,
            y: int,
            vx: int, 
            vy: int,
            colors: List[Tuple[int, int, int]],
            lifespan: int,
            move,
            next_color=None,
            next_char=None,
            param=None,
            on_create=None,
            on_each=None,
            on_destroy=None
        ) -> None:
        self.chars = chars
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colors = colors
        self.time = 0
        self.lifespan = lifespan
        
        self._move = move
        self._next_color = (
            self._default_next_color if next_color is None else next_color)
        self._next_char = (
            self._default_next_char if next_char is None else next_char)
        self._last = None
        self.param = param
        self._on_create = on_create
        self._on_each = on_each
        self._on_destroy = on_destroy

    @staticmethod
    def _default_next_char(p: Particle):
        """Default next character - linear progression through each char."""
        return p.chars[(len(p.chars) - 1) * p.time // p.lifespan]
    
    @staticmethod
    def _default_next_color(p: Particle):
        """Default next color - linear progression through each color."""
        return p.colors[(len(p.colors) - 1) * p.time // p.lifespan]

    def last(self):
        """The last attributes returned for this particle - typicall used
        for clearing out the particle on the next frame."""
        return self._last
    
    def next(self):
        """The set of attributes for this particle for the next frame to be 
        rendered.
        """
        # Get the next particle's details.
        x, y = self._move(self)
        char = self._next_char(self)
        color = self._next_color(self)
        self._last = char, x, y, (color[0], color[1], color[2])
        self.time += 1
        
        # Trigger any configured events.
        if self.time == 1 and self._on_create is not None:
            self._on_create(self)
        elif self.lifespan == self.time and self._on_destroy is not None:
            self._on_destroy(self)
        elif self._on_each is not None:
            self._on_each(self)
            
        return self._last


class ParticleEmitter:
    """An emitter for a particle system to create a set of `Particle` objects.
    After initialization, the emitter will be called once per frame to be 
    displayed on the Console.
    """
    
    def __init__(
            self,
            x: int,
            y: int,
            count: int,
            new_particle,
            spawn,
            lifespan,
            area,
            blend=False
        ) -> None:
        self._x = x
        self._y = y
        self._count = count
        self._new_particle = new_particle
        self._lifespan = lifespan
        self._area = area
        self.particles = []
        self.time_left = spawn
        self._blend = blend
        
    @staticmethod
    def _find_color(p, start_index, console_data):
        """Helper function to find an existing color in the particle palette."""
        pass
    
    def update(self, consoles):
        """Draw a new frame for the particle system."""
        # Spawn new particles if required.
        if self.time_left > 0:
            self.time_left -= 1
            for _ in range(self._count):
                new_particle = self._new_particle()
                if new_particle is not None:
                    self.particles.append(new_particle)
        
        cam_x, cam_y = self._area.camera.get_camera_pos()
        
        # Now draw all of them.
        # FIXME: Figure out how to constrain rendering to passables
        for particle in self.particles:
            last = particle.last()
            if last is not None:
                char, x, y, fg = last
                bg = self._area.area_model.get_bg_color(x-cam_x, y-cam_y)
                consoles['ROOT'].print(x-cam_x, y-cam_y, " ", fg, bg)
            
            if particle.time < particle.lifespan:
                # Draw the new one
                char, x, y, fg = particle.next()
                bg = self._area.area_model.get_bg_color(x-cam_x, y-cam_y)
                consoles['ROOT'].print(x-cam_x, y-cam_y, char, fg, bg)
            else:
                self.particles.remove(particle)


class ParticleEffect(Effect):

    def __init__(
            self, 
            x: int, 
            y: int,
            lifespan: int,
            area,
            **kwargs
        ) -> None:
        super().__init__(**kwargs)
        self._x = x
        self._y = y
        self._lifespan = lifespan
        self._area = area
        self._active_emitters = []
        self.reset()
        
    def reset(self):
        pass
    
    @property
    def emitters(self):
        return self._active_emitters
    
    def _update(self, frame_n: int, consoles):
        for emitter in copy(self._active_emitters):
            if len(emitter.particles) > 0 or emitter.time_left > 0:
                emitter.update(consoles)
            else:
                self._active_emitters.remove(emitter)
                if len(self._active_emitters) < 0:
                    self._manager.model.effect_flag = False
    
    @property
    def stop_frame(self):
        return self._stop_frame