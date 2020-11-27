from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from animation import Animation


class AnimationManager:
    
    def __init__(self) -> None:
        self.running: bool = False
        self.queue: List[Animation] = []
    
    def loop(self) -> Optional[Animation]:
        while self.running:
            if len(self.queue) == 0:
                self.stop()
            else:
                next: Animation = self.queue.pop()
                next = next()
                return next
                if next.looping:
                    self.queue.insert(0, next)
    
    def add_animation(self, animation: Animation) -> None:
        self.queue.append(animation)
        if not self.running:
            self.start()
    
    def clear_queue(self) -> None:
        self.queue.clear()
    
    def start(self) -> None:
        self.running = True
        self.loop()
    
    def stop(self) -> None:
        self.running = False