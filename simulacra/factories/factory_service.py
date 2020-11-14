from __future__ import annotations
from typing import TYPE_CHECKING


class FactoryService:

    def __init__(self, body_fac, char_fac):
        self.body_factory = body_fac
        self.character_factory = char_fac
