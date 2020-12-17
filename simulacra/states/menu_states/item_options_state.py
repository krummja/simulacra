from __future__ import annotations
from typing import Any, List, Optional, TYPE_CHECKING
import tcod

from actions import common
from state import StateBreak
from states.base_menu_state import BaseMenuState
from views.menu_views.item_options_view import ItemOptionsView

if TYPE_CHECKING:
    from item import Item
    from entity import Entity
    from model import Model
    from view import View
    

class ItemOptionsState(BaseMenuState["Action"]):
    
    def __init__(self, item: Item) -> None:
        self._item = item
        self._player = self.manager_service.data_manager.query(entity="PLAYER")
        self._options = self._make_options()
        super().__init__(ItemOptionsView, self._options)
        
    def _make_options(self) -> List[Any]:
        _options = []
        if not self._item.is_equipped and self._item.owner is not None:
            _options.append('drop')
        if self._item.is_equippable:
            _options.append('equip')
        if self._item.is_equipped:
            _options.append('dequip')
        if len(_options) > 0:
            return _options
        else:
            pass
        
    def _opt_drop(self):
        return common.Nearby.Drop(self._player, self._item)
    
    def _opt_equip(self):
        return common.Equip(self._player, self._item)
    
    def _opt_dequip(self):
        return common.Dequip(self._player, self._item)
    
    def cmd_confirm(self):
        if self._options[self._selection] == 'drop':
            return self._opt_drop()
        if self._options[self._selection] == 'equip':
            return self._opt_equip()
        if self._options[self._selection] == 'dequip':
            return self._opt_dequip()