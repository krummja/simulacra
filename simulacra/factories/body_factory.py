from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Model
    from factories.factory_service import FactoryService


class BodyFactory:

    def __init__(
            self,
            model: Model,
            factory_service: FactoryService
        ) -> None:
        self.model = model
        self.factory_service = factory_service
