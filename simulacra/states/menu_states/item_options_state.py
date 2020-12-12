from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod

from states.base_menu_state import BaseMenuState
from views.menu_views.item_options_view import ItemOptionsView

if TYPE_CHECKING:
    from entity import Entity
    from model import Model
    from view import View
    

class ItemOptionsState(BaseMenuState["Action"]):
    
    def __init__(self, item_options: List[Entity]) -> None:
        super().__init__(ItemOptionsView, item_options)
    
    def cmd_confirm(self):
        pass