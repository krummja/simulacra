from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Type

from config import *
from data.interface_elements import *
from factories.factory_service import FactoryService
from panel import Panel
from view import View
from rendering import render_area_tiles, render_visible_entities

if TYPE_CHECKING:
    from tcod.console import Console
    from component import Component
    from entity import Entity
    from model import Model
    from state import State


# TODO: What I need is a listing of all possible UI-renderable data sources.
# The idea being that the GUI either has 'passive' informational elements, or
# modal objects and menus that raise based on input choices or state changes.
    

class ModalView(View):
    
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self._opt_list = []
        self._entity_list = []
        self._clear = False
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        
        if self._state._case == 'delete':
            #! Create a modal panel to display the warning.
            delete = Panel(**{
                'position': ("center", "center"),
                'size': {'width': 25, 'height': 5},
                'style': {'framed': True,
                          'fg': (255, 0, 0)}
                })
            delete.on_draw(consoles)
            
            #! Print options to the modal display.
            consoles['ROOT'].print(
                delete.x + 1, 
                delete.y + 1, 
                "this is *irreversible*!\n \nare you sure? (y/n/esc)",
                fg=(255, 0, 0)
                )
            
        elif self._state._case == 'examine':
            consoles['ROOT'].clear()
            self._state._stage_view.draw(consoles)
            
            item_y = 0
            nearby_items = self._state.get_nearby_items_list()
            examine = Panel(**{
                'position': ("center", "right"),
                'offset': {'x': -38},
                'size': {'width': 25, 'height': len(nearby_items) + 4},
                'style': {'title': " nearby ",
                          'framed': True,
                          'fg': (255, 255, 255)}
                })
            examine.on_draw(consoles)
            
            focused = (255, 0, 255)
            unfocused = (255, 255, 255)
            for item in nearby_items:
                consoles['ROOT'].print(
                    x=examine.x + 2, 
                    y=examine.y + item_y + 2,
                    string=item.noun_text,
                    fg=focused if item_y == self._state.list_index else unfocused
                    )
                item_y += 1

        elif self._state._case == 'options':
            item_y = 0
            options = Panel(**{
                'position': ("center", "right"),
                'offset': {'x': -63},
                'size': {'width': 25, 'height': len(self._opt_list) + 4},
                'style': {'title': " options ",
                          'framed': True,
                          'fg': (255, 255, 255)}
                })
            options.on_draw(consoles)

            focused = (255, 0, 255)
            unfocused = (255, 255, 255)
            for option in self._opt_list:
                consoles['ROOT'].print(
                    x = options.x + 2,
                    y = options.y + item_y + 2,
                    string=option,
                    fg = focused if item_y == self._state.list_index else unfocused
                )
                item_y += 1
