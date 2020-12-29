# pylint: skip-file
import unittest

from graph_engine.graph import Graph
from graph_engine.vertex import Vertex
from graph_engine.generator import Generator
from graph_engine.production import Production

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
        self.assertEqual(self.g._vertices['u1'].degree, 1)
        self.assertEqual(self.g._vertices['u2'].degree, 1)

    def testDeleteEdge(self):

        self.assertFalse(self.g.delete_edge('aaa', 'bbb'))
        self.g.add_edge(Vertex('u1', 'A'), Vertex('u2', 'B'))

        u1 = self.g._vertices['u1']
        u2 = self.g._vertices['u2']

        self.assertFalse(self.g.delete_edge('u1', 'bbb'))

        self.assertTrue(self.g.delete_edge('u1', 'u2'))

        self.assertTrue(u2 not in self.g._edges['u1'])
        self.assertTrue(u2 not in self.g._neighbors['u1'])

        self.assertEqual(u1.degree, 0)
        self.assertEqual(u2.degree, 0)

    def testHasEdgeBetweenVertices(self):
        self.g.add_edge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.assertTrue(self.g.has_edge_between_vertices('u0', 'u1'))

    def testRepr(self):
        self.assertEqual(self.g.__repr__(), "digraph {\n\n}")
        self.g.add_vertex(Vertex('u1', 'A'))
        self.g.add_edge('u1', Vertex('u2', 'B'))
        self.g.add_edge('u2', Vertex('u3', 'C'))
        print(self.g)

    def testApplyProduction(self):
        g = Graph()
        g.add_edge(Vertex('g0', 'A'), Vertex('g1', 'B'))
        g1 = g._vertices['g1']

        lhs = Graph()
        lhs.add_edge(Vertex('l0', 'A', 1), Vertex('l1', 'B', 1))

        rhs = Graph()
        rhs.add_edge(Vertex('r0', 'A', 1), Vertex('r1', 'C'))
        p = Production(lhs,rhs)

        gen = Generator()
        gen._apply_production(g, p, {'l0':'g0','l1':'g1'})

        self.assertEqual(len(g._vertices), 2)
        self.assertEqual(g._vertices['v1'].label, 'C')

        self.assertEqual(len(g._edges['g0']), 1)
        self.assertEqual(g._edges['g0'][0].vid, 'v1')
        self.assertEqual(g._vertices['v1'].label, 'C')

        self.assertNotIn(g1, g._edges['g0'])

        self.assertNotIn('g1', g._vertices)

if __name__ == '__main__':
    unittest.main()