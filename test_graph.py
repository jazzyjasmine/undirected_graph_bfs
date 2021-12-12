from typing import Tuple
import graph
import unittest
import copy
import random
import collections


class testGraph(unittest.TestCase):
    """Tests the Graph class.

    Attributes:
        graph ('Graph'): An instance of
            the Graph class, same as
            Figure 1 in the homework
            instruction.
        existed_nodes (list): A list
            of all nodes in Figure 1.
        expected_bfs_result_dict (dict):
            A dictionary whose key is
            the node id of Figure 1 and
            the corresponding value is
            the correct (node, distance)
            pairs by bfs. Used to examine
            if the bfs result is correct.

    """

    def setUp(self) -> None:
        """Sets up attributes before tests."""
        self.graph = graph.Graph([(6, 4), (4, 3), (4, 5),
                                  (3, 2), (5, 2), (5, 1), (1, 2)])
        self.existed_nodes = [6, 4, 3, 5, 2, 1]
        self.expected_bfs_result_dict = \
            {6: [(4, 1), (3, 2), (5, 2), (2, 3), (1, 3)]
                , 4: [(6, 1), (3, 1), (5, 1), (2, 2), (1, 2)]
                , 3: [(6, 2), (4, 1), (5, 2), (2, 1), (1, 2)]
                , 5: [(6, 2), (4, 1), (3, 2), (2, 1), (1, 1)]
                , 2: [(6, 3), (4, 2), (3, 1), (5, 1), (1, 1)]
                , 1: [(2, 1), (5, 1), (3, 2), (4, 2), (6, 3)]}

    def test_add_node(self) -> None:
        """Tests if add_node method works properly."""
        original_graph = copy.deepcopy(self.graph)

        new_node1 = 9  # a node not on the graph
        self.graph.add_node(new_node1)
        self.assertIn(new_node1, self.graph.adjacency_dict)
        del self.graph.adjacency_dict[new_node1]
        self.assertEqual(self.graph, original_graph)

        new_node2 = 4  # a node on the graph
        self.graph.add_node(new_node2)
        self.assertEqual(self.graph, original_graph)

    def add_edge_helper(self, new_edge: Tuple[int, int],
                        original_graph: graph.Graph) -> None:
        """Determines if an edge can be added properly.

        Args:
            new_edge: The edge to be added.
            original_graph: The graph before adding an edge.

        """
        self.graph.add_edge(new_edge)

        for index, node in enumerate(new_edge):
            pair_node_index = 1 if index == 0 else 0
            pair_node = new_edge[pair_node_index]

            self.assertIn(node, self.graph.adjacency_dict)
            self.assertIn(pair_node, self.graph.adjacency_dict[node])

            if node not in original_graph:
                del self.graph.adjacency_dict[node]
            else:
                self.graph.adjacency_dict[node].remove(new_edge[pair_node_index])

        self.assertEqual(original_graph, self.graph)

    def test_add_edge(self) -> None:
        """Tests if add_edge method works properly"""
        original_graph = copy.deepcopy(self.graph)
        new_edges = [(7, 8),  # a new edge with both nodes not on the graph
                     (4, 9),  # a new edge with only one node on the graph
                     (3, 5)]  # a new edge with both nodes on the graph
        for new_edge in new_edges:
            self.add_edge_helper(new_edge, original_graph)

        self.graph.add_edge((4, 3))  # an existed edge
        self.assertEqual(original_graph, self.graph)

    def test_contains(self) -> None:
        """Tests if __contains__ works properly"""
        for existed_node in self.existed_nodes:
            self.assertIn(existed_node, self.graph)

        non_existed_nodes = [random.randint(7, 100), random.randint(-100, 0)]
        for non_existed_node in non_existed_nodes:
            self.assertFalse(non_existed_node in self.graph)

    def test_subscript_operator(self) -> None:
        """Tests if subscript operator [] works properly"""
        self.assertSetEqual(self.graph[6], {4})
        self.assertSetEqual(self.graph[4], {3, 5, 6})
        self.assertSetEqual(self.graph[3], {2, 4})
        self.assertSetEqual(self.graph[5], {1, 2, 4})
        self.assertSetEqual(self.graph[2], {1, 3, 5})
        self.assertSetEqual(self.graph[1], {2, 5})
        with self.assertRaises(ValueError):
            self.graph[10]

    def test_bfs(self) -> None:
        """Tests if bfs method works properly"""
        for existed_node in self.existed_nodes:
            bfs_result = self.graph.bfs(existed_node)
            self.assertListEqual(sorted(bfs_result),
                                 sorted(self.expected_bfs_result_dict[existed_node]))

            duplicate_pairs = [item
                               for item, count in
                               collections.Counter(bfs_result).items()
                               if count > 1]
            self.assertFalse(duplicate_pairs)

        with self.assertRaises(ValueError):
            self.graph.bfs(-3)

    def get_correct_distance(self,
                             first_node: int,
                             second_node: int) -> int:
        """Gets the correct(expected) distance between two nodes.

        Args:
            first_node (int): The first node on the graph.
            second_node (int): The second node on the graph.

        Returns:
            The correct distance between two nodes.

        """
        target_pair_list = [pair
                            for pair in self.expected_bfs_result_dict[first_node]
                            if pair[0] == second_node]
        return target_pair_list[0][1]

    def test_distance(self) -> None:
        """Tests if distance methods works properly"""
        for first_node_index in range(len(self.existed_nodes)):
            for second_node_index in range(first_node_index + 1, len(self.existed_nodes)):
                first_node = self.existed_nodes[first_node_index]
                second_node = self.existed_nodes[second_node_index]

                distance = self.graph.distance(first_node, second_node)

                self.assertEqual(distance,
                                 self.get_correct_distance(first_node, second_node))
                self.assertEqual(distance,
                                 self.get_correct_distance(second_node, first_node))

        with self.assertRaises(ValueError):
            self.graph.distance(10, 20)

    def test_iterator(self) -> None:
        """Tests if the Graph is iterable"""
        self.graph.all_nodes.sort()
        for node_id in range(1, 7):
            self.assertEqual(next(self.graph), node_id)
        self.assertRaises(StopIteration, next, self.graph)
