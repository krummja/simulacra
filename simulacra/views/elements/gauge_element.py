from __future__ import annotations
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from views.elements.base_element import BaseElement, BaseRenderable

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model


class GaugeElement(BaseRenderable):
    
    def __init__(self, element: BaseElement) -> None:
        super().__init__(element)
    
    def draw_contents(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(
            self.x, self.y, 
            "This is a gauge!", 
            )