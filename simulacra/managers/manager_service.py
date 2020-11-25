from __future__ import annotations
from typing import TYPE_CHECKING

from managers.animation_manager import AnimationManager
from managers.interface_manager import InterfaceManager


class ManagerService:

    def __init__(self) -> None:
        self.animation_manager = AnimationManager()
        self.interface_manager = InterfaceManager()