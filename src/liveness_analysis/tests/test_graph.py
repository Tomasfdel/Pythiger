import unittest

from liveness_analysis.graph import Graph


class TestSymbolTable(unittest.TestCase):
    def setUp(self):
        self.graph = Graph[int]()

    def test_add_node(self):
        for value in range(5):
            node = self.graph.add_node(value)
            self.assertEqual(value, node.information)

    def test_get_nodes(self):
        for value in range(5):
            self.graph.add_node(value)

        nodes = self.graph.get_nodes()

        self.assertEqual(len(nodes), 5)
        self.assertEqual(list(range(5)), [node.information for node in nodes])

    def test_node_successors(self):
        origin = self.graph.add_node(0)
        destination = self.graph.add_node(1)
        unrelated = self.graph.add_node(2)

        self.assertEqual(self.graph.node_successors(origin), [])

        self.graph.add_edge(origin, destination)

        self.assertIn(destination, self.graph.node_successors(origin))
        self.assertNotIn(unrelated, self.graph.node_successors(origin))

    def test_node_predecessors(self):
        origin = self.graph.add_node(0)
        destination = self.graph.add_node(1)
        unrelated = self.graph.add_node(2)

        self.assertEqual(self.graph.node_predecessors(origin), [])

        self.graph.add_edge(origin, destination)

        self.assertIn(origin, self.graph.node_predecessors(destination))
        self.assertNotIn(unrelated, self.graph.node_predecessors(destination))

    def test_add_edge_idempotence(self):
        origin = self.graph.add_node(0)
        destination = self.graph.add_node(1)

        self.assertEqual(self.graph.node_successors(origin), [])

        self.graph.add_edge(origin, destination)
        self.assertIn(destination, self.graph.node_successors(origin))

        self.graph.add_edge(origin, destination)
        self.assertIn(destination, self.graph.node_successors(origin))

        self.graph.remove_edge(origin, destination)
        self.assertEqual(self.graph.node_successors(origin), [])

    def test_node_adjacent(self):
        origin = self.graph.add_node(0)
        middle = self.graph.add_node(1)
        destination = self.graph.add_node(2)

        self.assertEqual(self.graph.node_adjacent(middle), [])

        self.graph.add_edge(origin, middle)
        self.assertIn(origin, self.graph.node_adjacent(middle))
        self.assertIn(middle, self.graph.node_adjacent(origin))

        self.graph.add_edge(middle, destination)
        self.assertIn(middle, self.graph.node_adjacent(destination))
        self.assertIn(destination, self.graph.node_adjacent(middle))

    def test_node_adjacent_back_and_forth_edges(self):
        node1 = self.graph.add_node(0)
        node2 = self.graph.add_node(1)

        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node2, node1)

        self.assertEqual(len(self.graph.node_adjacent(node1)), 1)
        self.assertEqual(len(self.graph.node_adjacent(node2)), 1)

    def test_node_goes_to(self):
        origin = self.graph.add_node(0)
        destination = self.graph.add_node(1)

        self.assertFalse(self.graph.node_goes_to(origin, destination))
        self.assertFalse(self.graph.node_goes_to(destination, origin))

        self.graph.add_edge(origin, destination)
        self.assertTrue(self.graph.node_goes_to(origin, destination))
        self.assertFalse(self.graph.node_goes_to(destination, origin))

        self.graph.remove_edge(origin, destination)
        self.assertFalse(self.graph.node_goes_to(origin, destination))
        self.assertFalse(self.graph.node_goes_to(destination, origin))

    def test_node_degree_single_edge(self):
        origin = self.graph.add_node(0)
        destination = self.graph.add_node(1)

        self.assertEqual(self.graph.node_degree(origin), 0)
        self.assertEqual(self.graph.node_degree(destination), 0)

        self.graph.add_edge(origin, destination)
        self.assertEqual(self.graph.node_degree(origin), 1)
        self.assertEqual(self.graph.node_degree(destination), 1)

        self.graph.remove_edge(origin, destination)
        self.assertEqual(self.graph.node_degree(origin), 0)
        self.assertEqual(self.graph.node_degree(destination), 0)

    def test_node_degree_back_and_forth_edge(self):
        node1 = self.graph.add_node(0)
        node2 = self.graph.add_node(1)

        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node2, node1)

        self.assertEqual(self.graph.node_degree(node1), 2)
        self.assertEqual(self.graph.node_degree(node2), 2)
