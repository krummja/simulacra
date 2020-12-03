from __future__ import annotations
from typing import TYPE_CHECKING

import tcod

from managers.manager_service import ManagerService

if TYPE_CHECKING:
    from entity import Entity
    from component import Component
    from model import Model
    from managers.manager_service import DataManager
    from factories.factory_service import FactoryService


class TextFactory:
    
    pass