import unittest

from graph_engine.graph import Graph
from graph_engine.vertex import Vertex


class TestGraph(unittest.TestCase):
    
    def setUp(self):
        self.g = Graph()
        
    def testConstructor(self):
        self.assertTrue(len(self.g._vertices) == 0)
        self.assertTrue(len(self.g._edges) == 0)
        self.assertTrue(len(self.g._neighbors) == 0)

    def testAddVertex(self):
        v = self.g.add_vertex(Vertex('u1'))
        self.assertTrue('u1' in self.g._vertices)
        
    def testAddEdge(self):
        a = self.g.add_vertex(Vertex('u1', 'A'))
        b = self.g.add_vertex(Vertex('u2', 'B'))
        self.g.add_edge('u1', 'u2')
        
        self.assertTrue(b in self.g._edges['u1'])
        self.assertTrue(b in self.g._neighbors['u1'])
        self.assertEquals(self.g._vertices['u1'].degree, 1)
        self.assertEquals(self.g._vertices['u2'].degree, 1)
        
    def testDeleteEdge(self):
        
        self.assertFalse(self.g.delete_edge('aaa', 'bbb'))
        self.g.add_edge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        
        u1 = self.g._vertices['u1']
        u2 = self.g._vertices['u2']
        
        self.assertFalse(self.g.delete_edge('u1', 'bbb'))
        
        self.assertTrue(self.g.delete_edge('u1', 'u2'))
        
        self.assertTrue(u2 not in self.g._edges['u1'])
        self.assertTrue(u2 not in self.g._neighbors['u1'])
        
        self.assertEquals(u1.degree, 0)
        self.assertEquals(u2.degree, 0)

    def testHasEdgeBetweenVertices(self):
        
        self.g.add_edge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.assertTrue(self.g.has_edge_between_vertices('u0', 'u1'))

    def testRepr(self):
        self.assertEquals(self.g.__repr__(), "digraph {\n\n}")
        self.g.add_vertex(Vertex('u1', 'A'))
        self.g.add_edge('u1', Vertex('u2', 'B'))
        self.g.add_edge('u2', Vertex('u3', 'C'))
        print(self.g)

if __name__ == '__main__':
    unittest.main()