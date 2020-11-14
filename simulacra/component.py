from __future__ import annotations
from typing import Any, Dict, KeysView, ValuesView, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class Component(dict):

    ident = '<unset>'

    def __init__(self, owner: Entity):
        super().__init__()
        self.owner = owner
