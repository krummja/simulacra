from __future__ import annotations
from typing import Dict, Type, TYPE_CHECKING

from tcod import Console

from config import *
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

        self.character_panel = Panel(**{
            'position': ('top', 'right'),
            'size': {
                'width': SIDE_PANEL_WIDTH,
                'height': (SIDE_PANEL_HEIGHT // 3)
                },
            'style': {'framed': True}
            })

        self.player_info_panel = Panel(**{
            'parent': self.character_panel,
            'position': ('top', 'left'),
            'offset': {'x': 2, 'y': 2},
            'size': {'width': SIDE_PANEL_WIDTH-3, 'height': 4},
            })

        bar_config = {
            'parent': self.character_panel,
            'position': ('top', 'center'),
            'offset_x': 1, 'margin': 0, 'width': 24,
            'text_fg': (255, 255, 255)
            }

        # player_hp = self.model.entity_data['PLAYER']['ATTRIBUTES']['HEALTH']
        # player_ep = self.model.entity_data['PLAYER']['ATTRIBUTES']['ENERGY']
        # player_fp = self.model.entity_data['PLAYER']['ATTRIBUTES']['HUNGER']

        # player_attributes: Attributes = self.model.player.get_component('ATTRIBUTES')
        # player_hp = player_attributes.get_current_value(StatsEnum.Health)

        player_hp = 10
        player_ep = 10
        player_fp = 10

        self.hp_gauge = ElemGauge(
            **bar_config,
            offset_y=7, name="vit", text=f"{player_hp}",
            fullness=player_hp / player_hp,
            fg=(0x40, 0x80, 0), bg=(0x80, 0, 0)
            )

        self.ep_gauge = ElemGauge(
            **bar_config,
            offset_y=9, name="enr", text=f"{player_ep}",
            fullness=player_ep / player_ep,
            fg=(0x17, 0x57, 0xc2), bg=(0x05, 0x1e, 0x50)
            )

        self.fp_gauge = ElemGauge(
            **bar_config,
            offset_y=11, name="hgr", text=f"{player_fp}",
            fullness=player_fp / player_fp,
            fg=(0xfb, 0x60, 0), bg=(0x60, 0x25, 0)
            )

        mock_cur_xp = 226
        mock_needed_xp = 1000
        mock_xp = mock_cur_xp / mock_needed_xp
        self.xp_gauge = ElemGauge(
            **bar_config,
            offset_y=15, name="exp", text=f"{mock_cur_xp} / {mock_needed_xp}",
            fullness=mock_xp,
            fg=(0x80, 0xe6, 0xea), bg=(0x10, 0x83, 0x95)
            )

        self.nearby_panel = Panel(**{
            'position': ('top', 'right'),
            'offset': {'y': (SIDE_PANEL_HEIGHT // 3)},
            'size': {'width': SIDE_PANEL_WIDTH, 'height': 8},
            'style': {'framed': True}
            })

        self.inventory_panel = Panel(**{
            'position': ('bottom', 'right'),
            'size': {
                'width': SIDE_PANEL_WIDTH,
                'height': (SIDE_PANEL_HEIGHT // 2) + 2
                },
            'style': {'framed': True}
            })

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

        self.hp_gauge.draw(consoles)
        self.ep_gauge.draw(consoles)
        self.fp_gauge.draw(consoles)
        self.xp_gauge.draw(consoles)

        self.nearby_panel.on_draw(consoles)
        self.inventory_panel.on_draw(consoles)

        self.log_panel.draw(consoles)