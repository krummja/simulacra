from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

import random

import tcod
import time

from graphic import Graphic

if TYPE_CHECKING:
    from area import AreaLocation
    from particles.particle_system import ParticleSystem
    from tcod.console import Console


class Particle(Graphic):

    char = "*"
    color = (255, 255, 255)
    bg = (0, 0, 0)
    distance = 0

    def __init__(
            self,
            system: ParticleSystem,
            origin: AreaLocation,
            vx: int, vy: int,
            color: Tuple[int, int, int] = (255, 0, 255),
            lifespan: int = 4
        ) -> None:
        self.system = system
        self.x = origin.x
        self.y = origin.y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifespan = lifespan

    @property
    def is_dead(self) -> bool:
        if self.distance > self.lifespan:
            return True
        else:
            return False

    def move(self) -> None:
        d = random.randint(-1, 1)
        self.x += self.vx + d
        self.y += self.vy + d
        self.distance += 1
        time.sleep(0.003)
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        cam_x, cam_y = self.system.model.area.camera.get_camera_pos()
        consoles['EFFECTS'].clear()
        consoles['EFFECTS'].print(
            x=self.x - cam_x,
            y=self.y - cam_y,
            string=self.char,
            fg=self.color)

        consoles['EFFECTS'].blit(
            consoles['ROOT'],
            0, 0, 0, 0,
            fg_alpha=1.0,
            bg_alpha=0.0)
