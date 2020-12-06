from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Type

from collections import defaultdict

import time

from graphic import Graphic
from config import *
from data.interface_elements import *
from geometry import *
from rendering import *
from tcod import Console
from view import View

from views.stage_view import StageView
from views.elements.base_element import BaseElement, ElementConfig
from views.elements.elem_log import ElemLog
from views.elements.gauge_element import GaugeElement
from views.elements.list_element import ListElement
from views.elements.test_animation_element import AnimationElement, AnimationFrame

if TYPE_CHECKING:
    from states.effects_state import EffectsState
    from model import Model
    from state import State


class EffectsView(StageView):
    
    def __init__(self, state: EffectsState, model: Model) -> None:
        super().__init__(state, model)
        self._runtime = 0

    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        area = self.model.area_data.current_area
        
        state_text = "EFFECTS STATE"
        width = len(state_text)
        consoles['ROOT'].print((STAGE_PANEL_WIDTH - width) // 2, 1, state_text, (255, 0, 0))
        
        render_visible_particles(area, consoles)
        
        if self.state.manager.running:
            consoles['ROOT'].print(2, 2, "Running animation loop.", (255, 255, 255))
            
            if self._runtime < 100:
                self._runtime += 1
            else:
                self._runtime = 0
                self.state.manager.running = False
                self.state.cmd_quit()