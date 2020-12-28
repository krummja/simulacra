from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from particles.particle import Particle

if TYPE_CHECKING:
    from particles.particle_system import ParticleSystem


directions = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
    'up_left': (-1, -1),
    'down_left': (-1, 1),
    'up_right': (1, -1),
    'down_right': (1, 1),
}


class TestEffect:
        
    def __init__(self, p_system: ParticleSystem) -> None:
        self.p_system = p_system

    def fire(self):
        for direction in directions.values():
            self.p_system.add_particles(1, *direction)
