from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Model


class EffectsManager:
    
    def __init__(self, model: Model) -> None:
        self.model = model