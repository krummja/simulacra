from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy import record


class Component:
    
    def __init__(self) -> None:
        self._data = []
    
    @property
    def data(self):
        return np.array(self._data, dtype=[('uid', 'U10'), ('val', 'i4')])

    @property
    def record(self):
        return np.rec.array(self._data, dtype=[('uid', 'U10'), ('val', 'i4')])

    def set_data(self, uid: str, val: int) -> None:
        self._data.append((uid, val))
        
    def get_uids(self):
        return self.data['uid']
    
    def get_vals(self):
        return self.data['val']

    def __str__(self) -> str:
        return str(self._data)


test_component = Component()
test_component.set_data('foo', 10)
test_component.set_data('bar', 12)
test_component.set_data('baz', 8)
uids = test_component.get_uids()
vals = test_component.get_vals()

test_component.data['uid'] = 'test'

print(test_component)
print(uids)
print(vals)
print(np.rec.record.pprint(test_component.record))

test = np.array([('foo', 10), ('bar', 20)], dtype=[('uid', 'U10'), ('val', 'i4')])
test['uid'] = 'baz'
test['val'] = 20

print(test)

# NOTE: Use NP arrays as lookups, e.g. how I can look up tile data like
# ch, fg, bg = tiles_rgb["ch", "fg", "bg"][y, x]
# to unpack tile values at y, x