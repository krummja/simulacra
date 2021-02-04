from __future__ import annotations
import json


def load_prefab(definition):
    with open('./prefabs/' + definition) as f:
        data = json.load(f)
        return data
