from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console


class BarElement(BaseElement):
    
    def __init__(self) -> None:
        super().__init__(ElementConfig(
            
            ))
    
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        pass