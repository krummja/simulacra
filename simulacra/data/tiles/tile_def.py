from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from collections import defaultdict
from enum import Enum


class TileType(Enum):
    Wall = 0
    Floor = 1


class StyleDef(defaultdict):
    
    def __init__(
            self, 
            color: Tuple[int, int, int], 
            bg: Tuple[int, int, int]
        ) -> None:
        self['color'] = color
        self['bg'] = bg


class TileDef(defaultdict):
    
    def __init__(
            self,
            uid: str,
            tile_type: int,
            char: int,
            style: StyleDef
        ) -> None:
        self['uid'] = uid
        self['move_cost'] = tile_type
        self['transparent'] = tile_type
        self['char'] = char
        self['color'] = style['color']
        self['bg'] = style['bg']
    
    
class TileDictionary(defaultdict):
    
    def __init__(self, category: str) -> None:
        self.category = category
        self['wall'] = {}
        self['floor'] = {}
        
    def add_new_tile(self, uid: str, tile_type: int, char: int, style: StyleDef) -> None:
        _tile = TileDef(uid, tile_type, char, style)
        if tile_type == TileType.Floor:
            self['floor'][uid] = _tile
        elif tile_type == TileType.Wall:
            self['wall'][uid] = _tile


class ForestTileDictionary(TileDictionary):
    
    def __init__(self) -> None:
        super().__init__("forest")
