from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

import random
import time
import tcod
from engine.hues import COLOR
from engine.graphic import Graphic

if TYPE_CHECKING:
    import tcod.console as Console


# https://code.harrywykman.com/implementing-a-simple-particle-system-in-python-using-libtcod.html


max_particle_moves = 100
particles_per_update = 2


class Particle(Graphic):

    def __init__(
            self, 
            x: int, 
            y: int, 
            vx: int, 
            vy: int,
            char: str,
            color: Tuple[int, int, int]
        ) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.char = char
        self.color = color
        self.moves = 0

    def is_dead(self) -> bool:
        if self.moves > max_particle_moves:
            return True
        else:
            return False

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.moves += 1

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(
            x=self.x,
            y=self.y,
            string=self.char,
            fg=self.color,
        )


class ParticleSystem:
    
    def __init__(self, x: int, y: int) -> None:
        self.origin = x, y
        self.particles = []

    def update(self) -> None:
        x, y = self.origin
        for p in self.particles:
            p.move()
            if p.is_dead():
                self.particles.remove(p)

    def add_particles(self, number) -> None:
        for i in range(0, number):
            vx = random.randint(-2, 2)
            vy = random.randint(-2, 2)
            p = Particle(self.origin[0], self.origin[1], vx, vy, "*", COLOR['red'])
            self.particles.append(p)

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        for p in self.particles:
            p.on_draw(consoles)