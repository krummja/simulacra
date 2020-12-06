from __future__ import annotations  # type: ignore
from typing import Dict, List, TYPE_CHECKING

import time

from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from state import State
    from entity import Entity
    

class AnimationElement(BaseElement):
    
    def __init__(self, config: ElementConfig) -> None:
        super().__init__(config)
        self.frames = [
            AnimationFrame(2, 2),
        ]
        self.running = False
    
    def play(self, dx: int, dy: int, consoles: Dict[str, Console]):
        console = consoles['EFFECTS']
        while self.running:
            frame = AnimationFrame(2, 2)
            if frame.lifespan == 0:
                self.running = False
            else:
                console.clear()
                frame.x += dx
                frame.y += dy
                frame.draw_frame(console)
            
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        consoles['EFFECTS'].set_key_color((1, 1, 1))
        consoles['EFFECTS'].tiles_rgb["fg"][:] = (1, 1, 1)
        self.running = False
        self.play(1, 1, consoles)
        if self.running:
            consoles['EFFECTS'].blit(consoles['ROOT'], 0, 0, 0, 0)
    

class AnimationFrame:
    
    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            color = (255, 0, 255),
            lifespan = 10,
        ) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.lifespan = lifespan
        # self.dx = 0
        # self.dy = 0
    
    def draw_frame(self, console):
        # self.x += self.dx
        # self.y += self.dy
        self.lifespan -= 1
        console.print(self.x, self.y, "*", self.color)
        