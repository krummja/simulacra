

class SomeClass:
    
    def __init__(self):
        self.prop = 'bar'
        

class OtherClass:
    
    def __init__(self, prop):
        self.prop = prop
        

some_config = {}
other_config = {'prop': 'foo'}

some_class = SomeClass(**{})
other_class = OtherClass(**{'prop': 'foo'})
print(some_class.prop)
print(other_class.prop)