from enum import Enum


class Direction(Enum):
    here = (0, 0)
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)


class Node:
    
    def __init__(self, uid, position, w, h):
        if isinstance(position, Node):
            self.x = position.x
            self.y = position.y
            position.add_child(self)
        else:
            self.x = position[0]
            self.y = position[1]
        self.uid = uid
        self.w = w
        self.h = h
        self.parent = None
        self.children = []
        
    def add_child(self, node):
        self.children.append(node)
        node.parent = self
        

class Path:
    
    def __init__(
            self,
            position,
            direction, 
            offset=0
        ):
        self.nodes = []
        if isinstance(position, Node):
            self.root = position
            self.start_x = self.root.x
            self.start_y = self.root.y
            self.nodes = self.root.children
        else:
            self.root = None
            self.start_x = position[0]
            self.start_y = position[1]
            self.nodes = []
        self.direction = direction
        self.offset = offset
    
    @property
    def length(self):
        l = self.compute_length()
        if self.direction == Direction.up or self.direction == Direction.down:
            return l[1]
        else:
            return l[0]
    
    @property
    def major_axis(self):
        """Representation of the path's direction-defined vector component."""
        l = self.compute_major_axes()
        if self.direction == Direction.up or self.direction == Direction.down:
            return l[1] * self.direction.value[1]
        else:
            return l[0] * self.direction.value[0]
    
    @property
    def minor_axis(self):
        """Representation of the path's offset-defined vector component."""
    
    def compute_major_axes(self):
        """Compute the total length for each vector component, agnostic of 
        the path's direction attribute."""
        horizontal = 0
        vertical = 0
        for node in self.nodes:
            horizontal += node.w
            vertical += node.h
        return (horizontal, vertical)

    def compute_length(self):
        if self.root is not None:
            l_width = (self.root.w // 2) + (self.nodes[-1].w // 2)
            l_height = (self.root.h // 2) + (self.nodes[-1].h // 2)
            for node in self.nodes[:-1]:
                l_width += node.w
                l_height += node.h
            return (l_width, l_height)

    def compute_lerp(self):
        pass
    

node4 = Node('ROOT', (30, 30), 10, 10)
node1 = Node('a', node4, 10, 10)
node2 = Node('b', node4, 10, 10)
node3 = Node('c', node4, 20, 10)
path = Path(node4, Direction.down)

print(path.length)