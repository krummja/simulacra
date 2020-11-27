from __future__ import annotations
from typing import Dict, Type, TYPE_CHECKING

from tcod import Console
import tdl

from config import *
from data.interface_elements import *
from rendering import *
from panel import Panel
from view import View
from views.elements.elem_log import ElemLog
from views.elements.elem_gauge import ElemGauge
from stats import StatsEnum
from components.attributes import Attributes
from component import Component
from factories.factory_service import FactoryService

if TYPE_CHECKING:
    from state import State
    from model import Model


class StageView(View):

    def __init__(self, state: State, model: Model) -> None:
        super().__init__(state)
        self.model = model
        self.state = state
        self.factory_service = FactoryService()

        self.character_panel = Panel(**character_panel)
        self.player_info_panel = Panel(**player_info_panel, 
                                       parent=self.character_panel)

        player_hp = 10
        player_ep = 10
        player_fp = 10

        self.hp_gauge = ElemGauge(
            **bar_config,
            parent=self.character_panel,
            offset_y=7, name="vit", text=f"{player_hp}",
            fullness=player_hp / player_hp,
            fg=(0x40, 0x80, 0), bg=(0x80, 0, 0)
            )

        self.ep_gauge = ElemGauge(
            **bar_config,
            parent=self.character_panel,
            offset_y=9, name="enr", text=f"{player_ep}",
            fullness=player_ep / player_ep,
            fg=(0x17, 0x57, 0xc2), bg=(0x05, 0x1e, 0x50)
            )

        self.fp_gauge = ElemGauge(
            **bar_config,
            parent=self.character_panel,
            offset_y=11, name="hgr", text=f"{player_fp}",
            fullness=player_fp / player_fp,
            fg=(0xfb, 0x60, 0), bg=(0x60, 0x25, 0)
            )

        mock_cur_xp = 226
        mock_needed_xp = 1000
        mock_xp = mock_cur_xp / mock_needed_xp
        self.xp_gauge = ElemGauge(
            **xp_config,
            parent=self.character_panel,
            offset_y=15, name="exp", 
            text=f"{mock_cur_xp} / {mock_needed_xp}",
            fullness=mock_xp,
            fg=(0x80, 0xe6, 0xea), bg=(0x10, 0x83, 0x95)
            )

        self.nearby_panel = Panel(**nearby_panel)
        self.inventory_panel = Panel(**inventory_panel)
        self.log_panel = ElemLog(self.model)

    def draw(self, consoles: Dict[str, Console]) -> None:
        area = self.model.area_data.current_area
        player = self.model.player
        if player.location:
            area.camera.camera_pos = player.location.xy

        update_fov(area)
        render_area_tiles(area, consoles)
        render_visible_entities(area, consoles)

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

        actors = self.model.area_data.current_area.actor_model.actors
        nearby_entities = [ent for ent in actors if ent.location.distance_to(*player.location.xy) <= 10]

        self.hp_gauge.draw(consoles)
        self.ep_gauge.draw(consoles)
        self.fp_gauge.draw(consoles)
        self.xp_gauge.draw(consoles)

        self.nearby_panel.on_draw(consoles)
        self.inventory_panel.on_draw(consoles)
        self.log_panel.draw(consoles)

        _y = 0
        nearby = self.get_nearby_list()
        for entity in nearby:        
            consoles['ROOT'].print(
                self.nearby_panel.x + 2,
                self.nearby_panel.y + 2 + _y,
                string=entity.noun_text,
                fg=(255, 255, 255)
                )
            _y += 1 if _y < 4 else 0

    def get_nearby_list(self):
        nearby = []
        actors = self.model.area_data.current_area.actor_model.actors
        player = self.model.player
        for actor in actors:
            if 1 <= actor.location.distance_to(*player.location.xy) <= 8:
                nearby.append(actor)
            elif actor.location.distance_to(*player.location.xy) > 8:
                try:
                    nearby.remove(actor)
                except ValueError:
                    pass
        return nearby