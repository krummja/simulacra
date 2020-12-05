from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from tcod.console import Console


class ParticleEmitter:
    """
    An emitter for a particle system to create a set of Particle objects for
    a ParticleEffect. After initialization, the emitter will be called once
    per frame to be displayed on the Console.
    """
    
    def __init__(
            self, 
            consoles: Dict[str, Console],
            x: int,
            y: int,
            count: int,
            new_particle,
            spawn,
            lifetime,
            blend: bool = False
        ) -> None:
        self._console = consoles['EFFECT']
        self._x = x
        self._y = y
        self._count = count
        self._new_particle = new_particle
        self._lifetime = lifetime
        self.particles = []
        self.time_left = spawn
        self._blend = blend
        
    @staticmethod
    def _find_color(particle, start_index, console_data):
        """Helper function to find an existing color in the particle palette."""
        pass
    
    def update(self) -> None:
        """Draw a new frame for the particle system."""
        
        # Spawn a new particle if necessary.
        if self.time_left > 0:
            self.time_left -= 1
            for _ in range(self._count):
                new_particle = self._new_particle()
                if new_particle is not None:
                    self.particles.append(new_particle)
        
        # Draw them to the console
        for particle in self.particles:
            last = particle.last()
            if last is not None:
                pass