from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

from collections import defaultdict

if TYPE_CHECKING:
    from entity import Entity


class Entity:
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.components = {'Component': 10}


test_data = {
    'entities': {
        'entity_1': Entity('entity_1'),
        'entity_2': Entity('entity_2')
    },
    'components': {}
}


def gather_components(data):
    results = {}
    for item in data:
        print(data[item].components)
    results.update(data)
    return results
    

test = gather_components(test_data['entities'])
print(test)


component_dict = {}
for entity in test_data['entities'].values():
    components = entity.components
    component_dict.update(components)

test_data['components'].update(component_dict)

