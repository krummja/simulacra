from __future__ import annotations
from typing import TYPE_CHECKING, Dict

from config import SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT

from engine.rendering import render_area_tiles, render_visible_entities, update_fov
from interface.elements.base_element import BaseElement, ElementConfig
from interface.elements.elem_log import ElemLog
from interface.elements.list_element import ListElement
from interface.views.view import View

from interface.views.panels.inventory_panel import InventoryPanel
from interface.views.panels.character_panel import CharacterPanel

from engine.entities.stat import StatsEnum

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.areas import Area
    from engine.model import Model
    from engine.states.state import State


class StageView(View):
    # pylint: disable=no-member

    def __init__(self, state: State, model: Model) -> None:
        super().__init__(state)
        self.model = model
        self.state = state
        self.manager = self.state.managers['data']

        self.nearby_panel = ListElement(
            config=ElementConfig(
                position=('top', 'right'),
                offset_y=(SIDE_PANEL_HEIGHT // 3),
                width=SIDE_PANEL_WIDTH, height=8,
                title="NEARBY", framed=True))

        self.inventory_panel = InventoryPanel(self.manager)

        self.character_panel = CharacterPanel(self.model, self.manager)

        self.log_panel = ElemLog(model=self.model)

    def draw(self, consoles: Dict[str, Console]) -> None:
        area = self.model.area_data.current_area
        player = self.model.player

        if player.location:
            area.camera.camera_pos = player.location.xy

        self.refresh(area, consoles)

        self.character_panel.draw(consoles)

        self.nearby_panel.update(self.get_nearby_actors())
        self.nearby_panel.draw(consoles)

        self.inventory_panel.draw(consoles)

        self.log_panel.draw(consoles)

    def refresh(self, area: Area, consoles: Dict[str, Console]) -> None:
        update_fov(area)
        render_area_tiles(area, consoles)
        render_visible_entities(area, consoles)

    def get_nearby_actors(self):
        nearby = []
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
