from __future__ import annotations
from typing import TYPE_CHECKING, Dict

from config import SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT

from interface.elements.base_element import BaseElement, ElementConfig
from interface.elements.gauge_element import GaugeElement

from engine.entities.stat import StatsEnum

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.model import Model
    from interface.data_manager import DataManager


class CharacterPanel:
    # pylint: disable=no-member

    def __init__(self, model: Model, manager: DataManager) -> None:
        self.model = model
        self.manager = manager

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

        player_stats = self.manager.query(entity="PLAYER", component="STATS")

        self.hp_gauge = GaugeElement(
            config=ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=18, height=1,
                offset_y=8, title="VIT"
                ),
            hue=(255, 0, 0),
            data=player_stats[StatsEnum.Health].display)

        self.ep_gauge = GaugeElement(
            config=ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=18, height=1,
                offset_y=10, title="ENG"
                ),
            hue=(25, 85, 195),
            data=player_stats[StatsEnum.Energy].display)

        self.fp_gauge = GaugeElement(
            config=ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=18, height=1,
                offset_y=12, title="HGR"
                ),
            hue=(250, 96, 0),
            data=(10.0, 10.0))

        self.xp_gauge = GaugeElement(
            config=ElementConfig(
                parent=self.character_panel,
                position=('top', 'left'),
                width=24, height=1,
                offset_y=15, title="EXP"
                ),
            hue=(130, 230, 230),
            data=(0, 1000))

    def draw(self, consoles: Dict[str, Console]) -> None:

        self.character_panel.draw(consoles)
        self.player_info_panel.draw(consoles)

        consoles['ROOT'].print(
            x=self.player_info_panel.x,
            y=self.player_info_panel.y,
            string=self.model.player.name,
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.player_info_panel.x,
            y=self.player_info_panel.y+2,
            string="Lv. 1",
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.player_info_panel.x+8,
            y=self.player_info_panel.y+2,
            string="Wanderer",
            fg=(255, 255, 255)
            )

        self.hp_gauge.draw(consoles)
        self.ep_gauge.draw(consoles)
        self.fp_gauge.draw(consoles)
        self.xp_gauge.draw(consoles)
