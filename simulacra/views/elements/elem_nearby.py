from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List, Dict, Tuple

from config import *
from panel import Panel

if TYPE_CHECKING:
    from item import Item
    from tcod.console import Console


# REFACTOR
class ElemExamineNearby(Panel):
    
    def __init__(self, items: List[Item]) -> None:
        super().__init__(**{
            'position': ('right', 'center'),
            'offset': {'x': -SIDE_PANEL_WIDTH-1},
            'size': {'width': 20, 'height': 3},
            'style': {'title': " nearby ", 'fg': (255, 255, 255)}})
        self.content = items
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        self.on_draw(consoles)