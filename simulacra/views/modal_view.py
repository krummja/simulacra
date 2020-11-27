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
    

class ModalView(View):
    
    def __init__(self, state: State) -> None:
        super().__init__(state)
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        if self._state._sort == 'Test':
            delete = Panel(**{'position': ("center", "center"),
                              'size': {'width': 25, 'height': 5},
                              'style': {'framed': True,
                                        'fg': (255, 0, 0)}})
            delete.on_draw(consoles)
            consoles['ROOT'].print(
                delete.x + 1, 
                delete.y + 1, 
                "this is *irreversible*!\n \nare you sure? (y/n/esc)",
                fg=(255, 0, 0)
            )