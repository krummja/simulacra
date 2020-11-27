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
    

"""
from Hauberk:

    case EventType.die:
        for (var i = 0; i < 10; i++) {
            effects.add(ParticleEffect(event.actor.x, event.actor.y, red));
        }
        break;
        
    
    GameResult makeResult(bool madeProgress) {
        var result = GameResult(madeProgress);
        result.events.addAll(_events);
        _events.clear();
        return result;
    }
"""