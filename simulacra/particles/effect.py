from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from abc import ABCMeta, abstractmethod

if TYPE_CHECKING:
    from tcod.console import Console
    from managers.effects_manager import EffectsManager


class Effect(metaclass=ABCMeta):
    
    def __init__(
            self,
            start_frame: int = 0,
            stop_frame: int = 0,
            delete_count=None
        ) -> None:
        self._manager = None
        self._start_frame = start_frame
        self._stop_frame = stop_frame
    
    def update(self, frame_no: int, consoles) -> None:
        if (frame_no >= self._start_frame and
                (self._stop_frame == 0 or frame_no < self._stop_frame)):
            self._update(frame_no, consoles)
    
    def register_manager(self, manager: EffectsManager) -> None:
        self._manager = manager
    
    @abstractmethod
    def _update(self, frame_no: int, consoles) -> None:
        pass