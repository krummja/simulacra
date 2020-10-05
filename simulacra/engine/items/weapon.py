from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from content.tiles import font_map
from engine.items import Item
from engine.components.offense import Offense

if TYPE_CHECKING:
    from engine.location import Location
