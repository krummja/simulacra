
class classproperty:
    """Implementation of class properties. Handy!"""
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
