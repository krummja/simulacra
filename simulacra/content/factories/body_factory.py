from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Model
    from factories.factory_service import FactoryService


class BodyFactory:

    def __init__(self) -> None:
        self._model = None

    @property
    def model(self) -> Model:
        return self._model
    
    @model.setter
    def model(self, value: Model) -> None:
        self._model = value