from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

from content.tiles.tilesets import tilesets
from engine.tiles.tile import Tile
from engine.tiles.tileset import TileSet

if TYPE_CHECKING:
    from engine.model import Model


class TileFactory:
    """Build either a single Tile or an entire Tile list from a Tileset.

    A Tileset is an object that exposes a dictionary of templates keyed to UIDs.
    The templates in the Tileset are built from an underlying Glyphset, which is
    a sliced subarray of the game's character map.
    """

    def __init__(self) -> None:
        self._instance_count = {}


# class TileFactory:

#     def __init__(self) -> None:
#         self._model = None
#         self.instance_count = {}

#     @property
#     def model(self) -> Model:
#         return self._model

#     @model.setter
#     def model(self, value: Model) -> None:
#         self._model = value

#     def build(self, uid: str, color=None, bg=None) -> None:
#         template = tile_templates[uid]
#         if template:
#             return self._assemble_template(template, color, bg)
#         else:
#             raise Exception(f"Could not find template for UID {uid}.")

#     def _assemble_template(self, template, color, bg) -> Tile:
#         instance_uid = 0

#         if template['uid'] in self.instance_count:
#             instance_uid = self.instance_count[template['uid']]
#             self.instance_count[template['uid']] += 1
#         else:
#             self.instance_count[template['uid']] = 1

#         instance_uid = template['uid'] + "_" + str(instance_uid)

#         new_tile = Tile(
#             uid=instance_uid,
#             move_cost=template['move_cost'].value,
#             transparent=template['transparent'].value,
#             char=template['char'],
#             color=color if color is not None else template['color'],
#             bg=bg if bg is not None else template['bg']
#             )

#         return new_tile

#     def convert_to_char_id(self, tile_id: int = 0) -> int:
#         return TilesetData().charmap[tile_id]

#     def convert_to_id_dict(self, tile_dict: Dict[str, int]) -> Dict[str, int]:
#         tile_id_dict = {}
#         for k, v in tile_dict.items():
#             tile_id_dict[v] = k
#         return tile_id_dict
