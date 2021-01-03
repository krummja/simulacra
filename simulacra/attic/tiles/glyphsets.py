from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from engine.tiles.glyphset import GlyphSet, GlyphsetType

if TYPE_CHECKING:
    pass


BOULDER_GS = GlyphSet(glyphset_type=GlyphsetType.Enumerate,
                      index=np.s_[16, 0:3])
