import aabbtree as abt

A = abt.AABB([(3, 5), (0, 2)])
B = abt.AABB([(1, 4), (1, 4)])
C = abt.AABB([(2, 5), (2, 5)])
D = abt.AABB([(0, 3), (2, 6)])

tree = abt.AABBTree()

tree.add(A, value="A")
tree.add(B, value="B")
tree.add(C, value="C")
tree.add(D, value="D")

print(tree)