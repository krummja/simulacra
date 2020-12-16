from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING

import copy

from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from item import Item
    from component import Component
    from tcod.console import Console


class InventoryElement(BaseElement):

    def __init__(self, config: ElementConfig, data: Component = None) -> None:
        super().__init__(config)
        if data is not None:
            _entries = [(k, v) for k, v in data.items()]
            self._data = [entry[1]['slot'] for entry in _entries]

    def draw_contents(self, consoles: Dict[str, Console]) -> None:
        pass
