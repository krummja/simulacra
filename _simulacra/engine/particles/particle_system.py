from __future__ import annotations  # type: ignore
from typing import Optional, Dict, List, Tuple, TYPE_CHECKING

import random
import time
from state import EffectsBreak
from particles.particle import Particle

if TYPE_CHECKING:
    from area import AreaLocation
    from model import Model
    from tcod.console import Console


class ParticleSystem:

    def __init__(self, model: Model, x: int, y: int) -> None:
        self.model = model
        self.origin: Tuple[int, int] = x, y
        self.particles: List[Particle] = []

    def update(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        for p in self.particles:
            p.move()
            # p.wiggle()
            if p.is_dead:
                self.particles.remove(p)

    def add_particles(self, number, vx, vy) -> None:
        for i in range(0, number):
            origin: AreaLocation = self.model.area[self.origin[0],
                                                   self.origin[1]]
            p = Particle(self, origin, vx, vy)
            self.particles.append(p)

    def draw(self, consoles: Dict[str, Console]) -> None:
        if not all(p.is_dead for p in self.particles):
            for p in self.particles:
                p.draw(consoles)
        else:
            self.model.effect_flag = False
            raise EffectsBreak