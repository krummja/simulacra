from __future__ import annotations
from typing import TYPE_CHECKING

from content.tiles.glyphsets import BOULDER_GS
from engine.tiles.tileset import TileSet, TileType

if TYPE_CHECKING:
    pass


BOULDER = TileSet(uid="boulder", tile_type=TileType.Wall, glyphset=BOULDER_GS)

tilesets = {
    BOULDER.uid: BOULDER
}
