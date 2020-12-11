class Structure:
    _fields = []
    def __init__(self, *args):
        for name, val in zip(self.__class__._fields, args):
            setattr(self, name, val)


class Point(Structure):
    _fields = ['x', 'y']

    def __str__(self):
        return f"({self.x}, {self.y})"
    

p = Point(2, 10)
print(p)