from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING
import time
import datetime
import numpy as np

from geometry import *

from config import CONSOLES
from tile import tile_graphic

if TYPE_CHECKING:
    from tcod.console import Console
    from action import Action


class AnimationFrame:
    
    def __init__(self, shape: Tuple[int, int], index: int) -> None:
        self.array = np.array(shape=shape, dtype=tile_graphic)


class Animation:
    
    def __init__(
            self,
            duration: float = 0.0,
            looping: bool = False
        ) -> None:
        self.looping = looping
        self.duration = duration
        self.playing: bool = False
        self.frames = []
    
    def play(self) -> None:
        # framecount: int = self.lerp(self.duration)
        self.playing = True
        while self.playing:
            for frame in self.frames:
                return frame
            self.stop()

    def stop(self) -> None:
        self.playing = False
    
    def lerp(self, value: int):
        pass
    

class TestAnimation(Animation):
    
    def __init__(self, duration):
        super().__(duration, False)
        self.frames = []