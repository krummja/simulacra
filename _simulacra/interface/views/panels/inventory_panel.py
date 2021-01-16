from __future__ import annotations
from typing import TYPE_CHECKING, Dict

from interface.elements.base_element import ElementConfig
from interface.elements.inventory_element import InventoryElement
from interface.elements.equipment_element import EquipmentElement

from interface.interface_elements import equipment_panel, inventory_panel

if TYPE_CHECKING:
    from tcod.console import Console
    from interface.data_manager import DataManager


class InventoryPanel:

    def __init__(self, manager: DataManager) -> None:
        self.manager = manager

        self.inventory_panel = InventoryElement(
            config=ElementConfig(**inventory_panel),
            data=self.manager.query(entity="PLAYER", component="INVENTORY"))

        self.equipment_panel = EquipmentElement(
            config=ElementConfig(**equipment_panel),
            data=self.manager.query(entity="PLAYER", component="EQUIPMENT"))

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.inventory_panel.draw(consoles)
        self.equipment_panel.draw(consoles)
