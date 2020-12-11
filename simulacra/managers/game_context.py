from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from factories.factory_service import FactoryService
    from managers.manager_service import ManagerService
    from model import Model


class GameContext:
    
    def __init__(self) -> None:
        self.model: Optional[Model] = None
        self.factory_service: Optional[FactoryService] = None
        self.manager_service: Optional[ManagerService] = None