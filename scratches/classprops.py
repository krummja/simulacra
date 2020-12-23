from __future__ import annotations


class classproperty:

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
    

class SomeClass:
    
    def __init__(self, name: str) -> None:
        self.name = name
        
    @classproperty
    def test_property(self) -> SomeClass:
        return SomeClass("test_name")


test = SomeClass.test_property.name
print(test)