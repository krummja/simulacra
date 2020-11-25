from __future__ import annotations
from typing import Dict, TYPE_CHECKING
import time
import datetime

from config import CONSOLES

if TYPE_CHECKING:
    from tcod.console import Console
    from action import Action


class Animation:
    
    def __init__(
            self,
            action: Action = None,
            duration: float = 0.0,
            looping: bool = False
        ) -> None:
        self.action = action
        self.looping = looping
        self.duration = duration
        self.playing: bool = False
    
    def play(self) -> None:
        framecount: int = self.lerp(self.duration)
        self.playing = True
        while self.playing:
            self.on_draw(framecount)
            self.stop()

    def stop(self) -> None:
        self.playing = False
    
    def lerp(self, value: int):
        pass
    
    def on_draw(self, frames: int) -> None:
        pass