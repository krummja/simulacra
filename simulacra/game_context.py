from __future__ import annotations
from typing import TYPE_CHECKING
from managers.animation_manager import AnimationManager
from factories.factory_service import FactoryService
from factories.interface_factory import InterfaceFactory

if TYPE_CHECKING:
    from model import Model


class GameContext:

    def __init__(self):
        self.model = None
        self.animation_manager = AnimationManager()
        self.interface_factory = InterfaceFactory()
    
    # def start_service(self, model: Model):
    #     self.model = model
    #     self.model.context = self
    #     self.factory_service = self.model.factory_service
    #     self.character_factory = self.factory_service.character_factory
    #     self.item_factory = self.factory_service.item_factory
    #     self.body_factory = self.factory_service.body_factory
    #     self.interface_factory = self.factory_service.interface_factory