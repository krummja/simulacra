from collections import defaultdict


class Component(defaultdict):
    
    def __init__(self, uid: str = "<unset>"):
        self.uid = uid
    
    
class SomeComponent(Component):
    
    def __init__(self, uid, a=None, b=None, c=None):
        super().__init__("COMPONENT")
        self['uid'] = uid
        self['a'] = a
        self['b'] = b
        self['c'] = c
        
    def copy(self):
        return SomeComponent(**self)
    

test = SomeComponent("COMPONENT_0", a="foo", b=1, c=2.2)
copy = test.copy()

print(copy)