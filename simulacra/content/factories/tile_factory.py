from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

import random

from engine.rendering.tile import Tile
from content.tiles.tile_defs import *
from engine.rendering.tilemap import TilesetData
from engine.rendering.hues import Color, COLOR

if TYPE_CHECKING:
    from engine.model import Model


class TileFactory:

    def __init__(self) -> None:
        self._model = None
        self.instance_count = {}
        self.wall_tiles = {}
        self.floor_tiles = {}

    @property
    def model(self) -> Model:
        return self._model

    @model.setter
    def model(self, value: Model) -> None:
        self._model = value

    def build(self, uid: str, color=None, bg=None) -> None:
        template = tile_templates[uid]
        if template:
            return self._assemble_template(template, color, bg)
        else:
            raise Exception(f"Could not find template for UID {uid}.")

    def _assemble_template(self, template, color, bg) -> Tile:
        instance_uid = 0

        if template['uid'] in self.instance_count:
            instance_uid = self.instance_count[template['uid']]
            self.instance_count[template['uid']] += 1
        else:
            self.instance_count[template['uid']] = 1

        instance_uid = template['uid'] + "_" + str(instance_uid)

        new_tile = Tile(
            uid=instance_uid,
            move_cost=template['move_cost'].value,
            transparent=template['transparent'].value,
            char=template['char'],
            color=color if color is not None else template['color'],
            bg=bg if bg is not None else template['bg']
            )

        return new_tile

    def convert_to_char_id(self, tile_id: int = 0) -> int:
        return TilesetData().charmap[tile_id]

    def convert_to_id_dict(self, tile_dict: Dict[str, int]) -> Dict[str, int]:
        tile_id_dict = {}
        for k, v in tile_dict.items():
            tile_id_dict[v] = k
        return tile_id_dict
