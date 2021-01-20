from __future__ import annotations

from ecstremity import Component


class Actor(Component):
    name = "ACTOR"

    def __init__(self) -> None:
        self._energy: int = 0

    @property
    def has_energy(self) -> bool:
        return self._energy >= 0

    def on_energy_consumed(self, event) -> None:
        pass
    
    def on_tick(self, event) -> None:
        pass
    
    def add_energy(self, value: int) -> None:
        self._energy += value
        if self._energy >= 0:
            self._energy = 0
            
    def reduce_energy(self, value: int):
        self.add_energy(value * -1)

    def __lt__(self, other: Actor) -> bool:
        return self._energy < other._energy
