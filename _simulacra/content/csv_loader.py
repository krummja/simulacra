from __future__ import annotations
from typing import Dict

import numpy as np

class PrefabData:
    """Data class for representing the layers making up a prefab."""

    def __init__(self, tiles: str, fg: str, bg: str) -> None:
        self.tiles = np.genfromtxt(tiles, delimiter=",", dtype=np.int)
        self.fg = np.genfromtxt(fg, delimiter=",", dtype=np.int)
        self.bg = np.genfromtxt(bg, delimiter=",", dtype=np.int)
        self.shape = self.tiles.shape


class CSVLoader:

    def __init__(self) -> None:
        self._prefab_path = 'simulacra/areas/prefabs/'
        self._prefabs: Dict[str, PrefabData] = {}

    def load_prefab_data(self, prefab_id: str) -> None:
        _tiles = self._prefab_path + prefab_id + '_Tilemap.csv'
        _fg = self._prefab_path + prefab_id + '_Foreground.csv'
        _bg = self._prefab_path + prefab_id + '_Background.csv'
        _prefab = PrefabData(_tiles, _fg, _bg)
        self._prefabs[prefab_id] = _prefab

    # use np.array.ravel to index 2D arrays as lists!
