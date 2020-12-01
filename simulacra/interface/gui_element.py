from __future__ import annotations
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from tcod.console import Console


class GUIElement:
    
    def __init__(self) -> None:
        pass
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        pass