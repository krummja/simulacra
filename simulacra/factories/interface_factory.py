from __future__ import annotations
from typing import TYPE_CHECKING

from views.elements.base_element import BaseElement, ElementConfig
from data.interface_elements import interface_templates

from managers.manager_service import ManagerService

if TYPE_CHECKING:
    from entity import Entity
    from component import Component
    from model import Model
    from managers.manager_service import DataManager
    from factories.factory_service import FactoryService


class InterfaceFactory:
    
    def build(self, uid: str, data):
        template = interface_templates[uid]
        if template:
            return self._assemble_template(template, data)
        else:
            raise Exception(f"Could not find template for UID {uid}.")
    
    def _assemble_template(self, template, data):
        new_config = ElementConfig(**template)
        new_instance = BaseElement(new_config, data)
        return new_instance