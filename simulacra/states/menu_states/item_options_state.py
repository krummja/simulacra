from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod

from state import StateBreak
from states.base_menu_state import BaseMenuState
from views.menu_views.item_options_view import ItemOptionsView

if TYPE_CHECKING:
    from entity import Entity
    from model import Model
    from view import View
    

class ItemOptionsState(BaseMenuState["Action"]):
    
    def __init__(self, item, *args) -> None:
        options = [_ for _ in item.options]
        super().__init__(ItemOptionsView, options)
        self.item = item
        self.args = args
    
    def cmd_confirm(self):
        commands = [opt.command for opt in self.item.options]
        player = self.manager_service.data_manager.query(entity="PLAYER")
        return commands[self.selection](player, self.item, *self.args)