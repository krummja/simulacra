from __future__ import annotations
from typing import TYPE_CHECKING

from config import *

from views.base_menu_view import BaseMenuView
from views.elements.base_element import ElementConfig

if TYPE_CHECKING:
    from entity import Entity
    from state import State
    

class EquipmentMenuView(BaseMenuView):
    
    def __init__(self, state: State) -> None:
        super().__init__(
            state=state,
            config=ElementConfig(
                position=("bottom", "right"),
                width=SIDE_PANEL_WIDTH,
                height=(SIDE_PANEL_HEIGHT // 2) + 2,
                fg=(255, 255, 255),
                title="EQUIPMENT",
                framed=True,
                frame_fg=(255, 0, 255)
                ))
        
    def draw_defaults(self, consoles: Dict[str, Console]) -> None:
        equipment_slots = [
            ('-', 'head'),
            ('-', 'torso'),
            ('-', 'shoulders'),
            ('-', 'back'),
            ('-', 'arms'),
            ('-', 'hands'),
            ('-', 'legs'),
            ('-', 'waist'),
            ('-', 'feet')
            ]
        
        y_index = 0
        for _ in range(len(equipment_slots)):
            
            consoles['ROOT'].print(
                x=self.x + 2,
                y=self.y + y_index + 2,
                string=equipment_slots[y_index][0],
                fg=(100, 100, 100)
                )
            
            consoles['ROOT'].print(
                x=self.x + 4,
                y=self.y + y_index + 2,
                string=equipment_slots[y_index][1],
                fg=(100, 100, 100)
                )
            y_index += 1
                
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        self.draw_help(consoles)
        self.draw_defaults(consoles)
        
        selected = (255, 0, 255)
        unselected = (255, 255, 255)
        
        data = self._state.data        
        
        y_index = 0        
        for _ in range(len(data)):
            if hasattr(data[y_index], 'char'):
                char = data[y_index].char
            else:
                char = ord(' ')

            if hasattr(data[y_index], 'color'):
                color = data[y_index].color
            else:
                color = (0, 0, 0)
            
            if hasattr(data[y_index], 'alt_fg'):
                fg = data[y_index].alt_fg
            else:
                if self._state.selection == y_index:
                    fg = selected
                else:
                    fg = unselected
                    
            if hasattr(data[y_index], 'noun_text'):
                text = data[y_index].noun_text
            else:
                text = data[y_index].uid
            
            consoles['ROOT'].print(
                x=self.x + 2, y=self.y + y_index + 2,
                string=chr(char),
                fg=color
                )
            
            consoles['ROOT'].print(
                x=self.x + 4, y=self.y + y_index + 2,
                string=text[0:14],
                fg=fg
                )
            y_index += 1
