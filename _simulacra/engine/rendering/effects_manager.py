"""ENGINE.RENDERING.Effects_Manager"""
from __future__ import annotations

from typing import TYPE_CHECKING

from engine.states.effects_state import EffectsBreak

if TYPE_CHECKING:
    from engine.model import Model


class EffectsManager:
    """Manager for particle effects.

    TODO: Is this class still needed?
    """

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
            raise EffectsBreak()

    def draw_next_frame(self, consoles):
        self._frame += 1
        for effect in self._effects:
            effect.update(self._frame, consoles)
