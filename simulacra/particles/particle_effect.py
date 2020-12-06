from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from abc import abstractmethod

from effect import Effect


class ParticleEffect(Effect):
    
    def __init__(self, console, x, y, lifetime, **kwargs) -> None:
        super().__init__(console, **kwargs)
        self._x = x
        self._y = y
        self._lifetime = lifetime
        self._active_systems = []
        self.reset()
    
    @abstractmethod
    def reset(self):
        pass
    
    def _update(self, frame_n):
        for system in copy(self._active_systems):
            if len(system.particles) > 0 or system.time_left > 0:
                system.update()
            else:
                self._active_systems.remove(system)
                
    @property
    def stop_frame(self):
        return self._stop_frame