from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import state

if TYPE_CHECKING:
    from model import Model


class EffectsManager:
    
    def __init__(
            self, 
            model: Model,
            duration=0,
            clear=True
        ) -> None:
        self.model = model
        self._effects = []
        self._frame = 0
        
    def add_effect(self, effect):
        effect.register_manager(self)
        self._effects.append(effect)
    
    def draw(self, consoles):
        if any(len(effect.emitters) > 0 for effect in self._effects):
            self.draw_next_frame(consoles)
        else:
            self.model.effect_flag = False
            raise state.EffectsBreak()
    
    def draw_next_frame(self, consoles):
        self._frame += 1
        for effect in self._effects:
            effect.update(self._frame, consoles)
