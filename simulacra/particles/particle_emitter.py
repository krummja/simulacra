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
                char, x, y, fg = last
                console_data = self._console[y, x]
                self._console.print(x, y, " ", fg)
            
            if particle.time < particle.lifetime:
                char, x, y, fg = particle.next()
                console_data = self._console[y, x]
                self._console.print(x, y, char, fg)
            
            else:
                self.particles.remove(particle)
                

class EmitterTest(ParticleEmitter):
    
    def __init__(self, consoles, x, y, lifetime, on_destroy=None):
        super().__init__(consoles, x, y, 1, self._next_particle, 1, lifetime)
        self._end_y = y
        self._acceleration = (self._end_y - self._y) // lifetime
        self._on_destroy = on_destroy
    
    def _next_particle(chars="*",
                       x=self._x,
                       y=self._y,
                       dx=0,
                       dy=self._acceleration,
                       colors=((255, 0, 255), (0, 0, 0)),
                       lifetime=self._lifetime,
                       move=self._move,
                       on_destroy=self._on_destroy)
    
    def _move(self, particle):
        particle.x += particle.dx
        particle.y += particle.dy
        if particle.y <= self._end_y:
            particle.y = self._end_y
            particle.time = self._lifetime - 1
        return int(particle.x), int(particle.y)