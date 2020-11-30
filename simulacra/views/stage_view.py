from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type

import tdl
from geometry import *
from component import Component
from components.attributes import Attributes
from config import *
from data.interface_elements import *
from factories.factory_service import FactoryService
from panel import Panel
from rendering import *
from stats import StatsEnum
from tcod import Console
from view import View

from views.elements.elem_gauge import ElemGauge
from views.elements.elem_log import ElemLog
from views.elements.elem_nearby import ElemExamineNearby

if TYPE_CHECKING:
    from model import Model
    from state import State


class StageView(View):

    def __init__(self, state: State, model: Model) -> None:
        super().__init__(state)
        self.model = model
        self.state = state
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        area = self.model.area_data.current_area
        player = self.model.player
        if player.location:
            area.camera.camera_pos = player.location.xy

        update_fov(area)
        render_area_tiles(area, consoles)
        render_visible_entities(area, consoles)
        
        self.factory_service.interface_factory.build('test_element').draw(consoles)
        self.factory_service.interface_factory.build('test_gauge').draw(consoles)