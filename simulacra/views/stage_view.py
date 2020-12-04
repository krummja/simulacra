from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type

from config import *
from data.interface_elements import *
from geometry import *
from rendering import *
from tcod import Console
from view import View

from views.elements.base_element import BaseElement, ElementConfig
from views.elements.elem_log import ElemLog
from views.elements.gauge_element import GaugeElement
from views.elements.list_element import ListElement

if TYPE_CHECKING:
    from model import Model
    from state import State


class StageView(View):

    def __init__(self, state: State, model: Model) -> None:
        super().__init__(state)
        self.model = model
        self.state = state
        self.factory = self.state.factory_service.interface_factory
        self.manager = self.state.manager_service.data_manager

        self.character_panel = BaseElement(
            ElementConfig(
                position=('top', 'right'),
                width=SIDE_PANEL_WIDTH,
                height=(SIDE_PANEL_HEIGHT // 3),
                framed=True
                ))

        self.player_info_panel = BaseElement(
            ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                offset_x=2, offset_y=2,
                width=SIDE_PANEL_WIDTH-3, height=4
                ))
        
        self.hp_gauge = GaugeElement(
            config = ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=18, height=1,
                offset_y=8, title="VIT"
                ), 
            hue=(255, 0, 0),
            data = (5.5, 10.0))

        self.ep_gauge = GaugeElement(
            config = ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=18, height=1,
                offset_y=10, title="ENG"
                ), 
            hue = (25, 85, 195),
            data = (10.0, 10.0))
        
        self.fp_gauge = GaugeElement(
            config = ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=18, height=1,
                offset_y=12, title="HGR"
                ), 
            hue = (250, 96, 0),
            data = (8.0, 10.0))

        self.xp_gauge = GaugeElement(
            config = ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=24, height=1,
                offset_y=15, title="EXP"
                ),
            hue = (130, 230, 230),
            data = (243, 1000))

        self.nearby_panel = ListElement(
            config = ElementConfig(
                position=('top', 'right'),
                offset_y=(SIDE_PANEL_HEIGHT // 3),
                width=SIDE_PANEL_WIDTH, height=8,
                title="NEARBY", framed=True
                ))

        self.inventory_panel = ListElement(
            config = ElementConfig(**inventory_panel),
            data = self.manager_service.data_manager.query(
                entity="PLAYER",
                component="INVENTORY",
                key="contents"))

        self.equipment_panel = ListElement(
            config = ElementConfig(**equipment_panel),
            data = [])
        
        self.log_panel = ElemLog(name="LOG PANEL", model=self.model)

    def draw(self, consoles: Dict[str, Console]) -> None:
        area = self.model.area_data.current_area
        player = self.model.player
        if player.location:
            area.camera.camera_pos = player.location.xy

        self.refresh(area, consoles)
        
        self.character_panel.draw(consoles)
        self.player_info_panel.draw(consoles)

        consoles['ROOT'].print(
            x=self.player_info_panel.x,
            y=self.player_info_panel.y,
            string=self.model.player.noun_text.upper(),
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.player_info_panel.x,
            y=self.player_info_panel.y+2,
            string="lv. 1",
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.player_info_panel.x+8,
            y=self.player_info_panel.y+2,
            string="WANDERER",
            fg=(255, 255, 255)
            )

        # GAUGES
        self.hp_gauge.draw(consoles)
        self.ep_gauge.draw(consoles)
        self.fp_gauge.draw(consoles)
        self.xp_gauge.draw(consoles)

        # PANEL FRAMES
        self.nearby_panel.update(self.get_nearby_actors())
        self.nearby_panel.draw(consoles)
        self.inventory_panel.draw(consoles)
        self.equipment_panel.draw(consoles)
        self.log_panel.draw(consoles)

    def refresh(self, area: Area, consoles: Dict[str, Console]) -> None:
        # TODO: Change this so that it doesn't have to take in 'area'
        update_fov(area)
        render_area_tiles(area, consoles)
        render_visible_entities(area, consoles)

    def get_nearby_actors(self):
        # TODO: Move this to the DataManager
        nearby = []
        area = self.model.area_data.current_area
        actors = self.model.area_data.current_area.actor_model.actors
        player = self.model.player
        for actor in actors:
            if len(nearby) < 4:
                if 1 <= actor.location.distance_to(*player.location.xy) <= 10:
                    nearby.append(actor)
                elif actor.location.distance_to(*player.location.xy) > 10:
                    try:
                        nearby.remove(actor)
                    except ValueError:
                        pass
        return nearby
