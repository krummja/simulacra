from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from math import pi, cos, sin
from random import uniform, randint
from engine.particles.particle import Particle, ParticleEmitter, ParticleEffect

if TYPE_CHECKING:
    from tcod.console import Console


class TestEmitter(ParticleEmitter):

    def __init__(
            self,
            x: int,
            y: int,
            lifespan: int,
            area,
            on_destroy=None
        ) -> None:
        super().__init__(x, y, 30, self._next_particle, 1, lifespan, area)
        self._end_y = y
        self._acceleration = 1.0 - (1.0 / lifespan)
        self._on_destroy = on_destroy

    def _next_particle(self):
        direction = uniform(-(2 * pi), 2 * pi)
        return Particle("***:. ",
                        self._x,
                        self._y,
                        sin(direction) * 8 / self._lifespan,
                        cos(direction) * 8 / self._lifespan,
                        [(255, 0, 255), (200, 0, 200), (155, 0, 155), (100, 0, 100)],
                        self._lifespan,
                        self._explode)

    def _explode(self, particle: Particle):
        particle.vy = particle.vy * self._acceleration + 0.03
        particle.vx *= self._acceleration
        particle.x += particle.vx
        particle.y += particle.vy
        return int(particle.x), int(particle.y)

    def _move(self, particle: Particle):
        particle.x += particle.vx
        particle.y += particle.vy
        if particle.y <= self._end_y:
            particle.y = self._end_y
            particle.time = self._lifespan - 1
        return int(particle.x), int(particle.y)


class TestEffect(ParticleEffect):

    def reset(self):
        self._active_emitters = []
        self._active_emitters.append(TestEmitter(self._x,
                                                 self._y,
                                                 10,
                                                 self._area))