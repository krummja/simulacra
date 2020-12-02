from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type

import tdl
from component import Component
from components.attributes import Attributes
from config import *
from data.interface_elements import *
from factories.factory_service import FactoryService
from geometry import *
from panel import Panel
from rendering import *
from stats import StatsEnum
from tcod import Console
from view import View

from views.elements.base_element import BaseElement, ElementConfig
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
        self.factory = self.state.factory_service.interface_factory
        self.manager = self.state.manager_service.data_manager
        self.character_panel = Panel(**character_panel)
        self.player_info_panel = Panel(**player_info_panel, 
                                       parent=self.character_panel)

        player_hp = 10
        player_ep = 10
        player_fp = 10
        mock_cur_xp = 226
        mock_needed_xp = 1000
        mock_xp = mock_cur_xp / mock_needed_xp
        
        self.hp_gauge = ElemGauge(
            "HP GAUGE",
            **bar_config,
            parent=self.character_panel,
            offset_y=7, title="vit", text=f"{player_hp}",
            fullness=player_hp / player_hp,
            fg=(0x40, 0x80, 0), bg=(0x80, 0, 0)
            )

        self.ep_gauge = ElemGauge(
            "EP GAUGE",
            **bar_config,
            parent=self.character_panel,
            offset_y=9, title="enr", text=f"{player_ep}",
            fullness=player_ep / player_ep,
            fg=(0x17, 0x57, 0xc2), bg=(0x05, 0x1e, 0x50)
            )

        self.fp_gauge = ElemGauge(
            "FP GAUGE",
            **bar_config,
            parent=self.character_panel,
            offset_y=11, title="hgr", text=f"{player_fp}",
            fullness=player_fp / player_fp,
            fg=(0xfb, 0x60, 0), bg=(0x60, 0x25, 0)
            )

        self.xp_gauge = ElemGauge(
            "XP GAUGE",
            **xp_config,
            parent=self.character_panel,
            offset_y=15, title="exp", 
            text=f"{mock_cur_xp} / {mock_needed_xp}",
            fullness=mock_xp,
            fg=(0x80, 0xe6, 0xea), bg=(0x10, 0x83, 0x95)
            )

        self.nearby_panel = Panel(name="NEARBY PANEL", **nearby_panel)
        self.inventory_panel = Panel(name="INVENTORY PANEL", **inventory_panel)
        self.equipment_panel = Panel(name="EQUIPMENT PANEL", **equipment_panel)
        self.log_panel = ElemLog(name="LOG PANEL", model=self.model)

        self.manager_service.interface_manager.register_element(self.hp_gauge)
        self.manager_service.interface_manager.register_element(self.ep_gauge)
        self.manager_service.interface_manager.register_element(self.fp_gauge)
        self.manager_service.interface_manager.register_element(self.xp_gauge)
        self.manager_service.interface_manager.register_element(self.nearby_panel)
        self.manager_service.interface_manager.register_element(self.inventory_panel)
        self.manager_service.interface_manager.register_element(self.equipment_panel)
        self.manager_service.interface_manager.register_element(self.log_panel)

        
    def draw(self, consoles: Dict[str, Console]) -> None:
        area = self.model.area_data.current_area
        player = self.model.player
        if player.location:
            area.camera.camera_pos = player.location.xy

        self.refresh(area, consoles)
        
        self.character_panel.on_draw(consoles)
        self.player_info_panel.on_draw(consoles)

        consoles['ROOT'].print(
            x=self.player_info_panel.x,
            y=self.player_info_panel.y,
            string=self.model.player.noun_text,
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
            string="test background",
            fg=(255, 255, 255)
            )

        actors = area.actor_model.actors
        nearby_entities = [ent for ent in actors if ent.location.distance_to(*player.location.xy) <= 10]

        # GAUGES
        self.hp_gauge.draw(consoles)
        self.ep_gauge.draw(consoles)
        self.fp_gauge.draw(consoles)
        self.xp_gauge.draw(consoles)


        # PANEL FRAMES
        self.nearby_panel.on_draw(consoles)
        self.inventory_panel.on_draw(consoles)
        self.equipment_panel.on_draw(consoles)
        self.log_panel.draw(consoles)

        # INVENTORY PANEL
        inventory = self.manager.query(entity="PLAYER", component="INVENTORY", key="contents")
        item_y = 0
        for item in inventory:
            consoles['ROOT'].print(
                self.inventory_panel.x + 2,
                self.inventory_panel.y + 2 + item_y,
                string=item.noun_text,
                fg=(255, 255, 255)
                )
            item_y += 1 if item_y < self.inventory_panel.size_height - 3 else 0

        # TODO: Make this into a ui element.
        # TODO: Display aggro state and combat info when in combat
        # e.g.:
        #*  *Test Character*   100/100          notices you (uwu)
        #! **Test Character**   20/100          actively attacking
        # NEARBY ENTITY PANEL
        entity_y = 0
        nearby_actors = self.get_nearby_actors()
        for entity in nearby_actors:
            consoles['ROOT'].print(
                self.nearby_panel.x + 2,
                self.nearby_panel.y + 2 + entity_y,
                string=entity.noun_text,
                fg=(255, 255, 255)
                )
            entity_y += 1 if entity_y < 3 else 0

    def refresh(self, area: Area, consoles: Dict[str, Console]) -> None:
        # TODO: Change this so that it doesn't have to take in 'area'
        update_fov(area)
        render_area_tiles(area, consoles)
        render_visible_entities(area, consoles)

    def get_nearby_actors(self):
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
