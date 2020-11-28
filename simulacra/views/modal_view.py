from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Type

from config import *
from data.interface_elements import *
from factories.factory_service import FactoryService
from panel import Panel
from view import View

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model
    from state import State


# TODO: What I need is a listing of all possible UI-renderable data sources.
# The idea being that the GUI either has 'passive' informational elements, or
# modal objects and menus that raise based on input choices or state changes.
    

class ModalView(View):
    
    def __init__(self, state: State) -> None:
        super().__init__(state)
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        
        if self._state._case == 'delete':
            delete = Panel(**{
                'position': ("center", "center"),
                'size': {'width': 25, 'height': 5},
                'style': {'framed': True,
                          'fg': (255, 0, 0)}
                })
            delete.on_draw(consoles)
            
            consoles['ROOT'].print(
                delete.x + 1, 
                delete.y + 1, 
                "this is *irreversible*!\n \nare you sure? (y/n/esc)",
                fg=(255, 0, 0)
                )
            
        elif self._state._case == 'examine':
            area = self._state.model.area_data.current_area
            area.item_model.get_nearby()
            
            item_y = 0
            nearby_items = area.nearby_items
            nearby_items = [item for sublist in nearby_items for item in sublist]
            
            examine = Panel(**{
                'position': ("center", "right"),
                'offset': {'x': -40},
                'size': {'width': 25, 'height': len(nearby_items) + 4},
                'style': {'title': " nearby ",
                          'framed': True,
                          'fg': (255, 255, 255)}
                })
            examine.on_draw(consoles)
            
            for item in nearby_items:
                consoles['ROOT'].print(
                    x=examine.x + 2, 
                    y=examine.y + item_y + 2,
                    string=item.noun_text,
                    fg=(255, 255, 255)
                    )