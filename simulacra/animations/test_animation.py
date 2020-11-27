from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from config import CONSOLES
from animation import Animation

if TYPE_CHECKING:
    from tcod.console import Console
    from action import Action
    

class TestAnimation(Animation):
    
    def __init__(
            self,
            duration: float = 0.0,
            looping: bool = False
        ) -> None:
        super().__init__(duration, looping)
    
    def on_draw(self, frames: int) -> None:
        print("Test Animation has played!")
        CONSOLES['EFFECT'].print(2, 2, "Test")
        CONSOLES['EFFECT'].blit(CONSOLES['ROOT'], 0, 0, 0, 0)