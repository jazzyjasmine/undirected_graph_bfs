from typing import Optional, List, Tuple
from collections import defaultdict, deque
from collections.abc import Iterator


class Graph(Iterator):
    """Undirected graph.

    Note that in this graph class, each node's id
    is an integer. The id is unique. A node is
    represented by its id.

    The graph does not contain multiple/duplicate
    edges according to the homework instruction.

    Attributes:
        adjacency_dict (dict): Works as an adjacency
            list, where each key stores a node id on
            the graph and the corresponding value (a
            set of node ids) stores all the adjacent
            (neighbor) nodes.
        all_nodes (list): The ids of all nodes on the
            graph.

    """

    def __init__(self, edges: List[Optional[Tuple[int, int]]]) -> None:
        """Constructs an instance of Graph.

        Args:
            edges: A list of edges, where each edge is in
                format (u,v). Note (u,v) is the same as (v,u).
        """
        self.adjacency_dict = defaultdict(set)
        self.all_nodes = []
        if not edges:
            return
        for edge in edges:
            self.add_edge(edge)
        self.update_all_nodes()

    def update_all_nodes(self) -> None:
        """Updates the all_nodes attribute"""
        self.all_nodes = [node for node in self.adjacency_dict.keys()]

    def is_edge_in_graph(self, edge: Tuple[int, int]) -> bool:
        """Checks if an edge is in the graph.

        Args:
            edge: The edge to be checked.

        Returns:
            True if the edge is in the graph, False otherwise.

        """
        return edge[0] in self.adjacency_dict and \
               edge[1] in self.adjacency_dict[edge[0]]

    def add_edge(self, edge: Tuple[int, int]) -> None:
        """Takes an edge and adds it to the graph.

        If the edge is already in the graph, then
        this function does nothing.

        Args:
            edge: The edge to be added to the graph.

        """
        if self.is_edge_in_graph(edge):
            return
        self.adjacency_dict[edge[0]].add(edge[1])
        self.adjacency_dict[edge[1]].add(edge[0])
        self.update_all_nodes()

    def add_node(self, new_node: int) -> None:
        """Takes a single node and adds it to the graph

        If the new node is already in the graph, then
        this function does nothing.

        Args:
            new_node: The node to be added in the graph.

        """
        if new_node in self:
            return
        self.adjacency_dict[new_node] = set()
        self.update_all_nodes()

    def bfs(self, start_node: int) -> List[Tuple[int, int]]:
        """Applies BFS algorithm and get (node, distance) pairs

        Args:
            start_node: The node to start from in BFS.

        Returns:
            A list of unique (node, distance) pairs for each
                node in the graph other than the starting node;
                The distance is the shortest number of edges
                between the starting node and the other node.
                If the other node is non reachable, then the
                distance is -1.

        Raises:
            ValueError: If the start node is not on the graph.

        """
        if start_node not in self:
            raise ValueError("Node not in graph!")

        distance_pairs = []
        distance = 0
        queue = deque([start_node])
        seen_nodes = {start_node}
        while queue:
            distance += 1
            for _ in range(len(queue)):
                current_node = queue.popleft()
                for current_node_neighbor in self.adjacency_dict[current_node]:
                    if current_node_neighbor in seen_nodes:
                        continue
                    seen_nodes.add(current_node_neighbor)
                    distance_pairs.append((current_node_neighbor, distance))
                    queue.append(current_node_neighbor)
        distance_pairs.extend([(node, -1)
                               for node in self.all_nodes
                               if node not in seen_nodes])
        return distance_pairs

    def distance(self, node1: int, node2: int) -> int:
        """Calculates the distance between two nodes.

        Args:
            node1: The id of a node on the graph.
            node2: The id of a node on the graph.

        Returns:
            The distance (shortest length of path)
            between the two nodes. If the two input
            nodes are the same, the distance between
            them is set to be 0.

        Raises:
            ValueError: If either node is not on
                the graph.

        """
        if node1 not in self or node2 not in self:
            raise ValueError("Node(s) not in graph!")
        if node1 == node2:
            return 0
        return [pair for pair in self.bfs(node1) if pair[0] == node2][0][1]

    def __getitem__(self, node: int) -> set:
        """Gets the neighbors or a node.

        Args:
            node: The id of a node on the graph.

        Returns:
            The neighbors (adjacent nodes) of the
                given node.

        Raises:
            ValueError: If the given node is not
                on the graph.

        """
        if node not in self:
            raise ValueError("Node not in graph!")
        return set(self.adjacency_dict[node])

    def __iter__(self) -> 'Graph':
        """Returns the iterator object itself.

        Returns:
            The iterator object (the graph).

        """
        return self

    def __next__(self) -> int:
        """Iterates the nodes in the graph.

        Returns:
            The id of the node.

        Raises:
            StopIteration: If all nodes
                have been iterated.

        """
        if len(self.all_nodes) > 0:
            return self.all_nodes.pop(0)
        else:
            raise StopIteration

    def __contains__(self, node: int) -> bool:
        """Determines if a node is in the graph.

        Args:
            node: The node to be checked.

        Returns:
            True if the node is in the graph,
                False otherwise.

        """
        return node in self.adjacency_dict

    def __eq__(self, other: 'Graph') -> bool:
        """Determines if two graphs are identical.

        Args:
            other: Another graph.

        Returns:
            True if two graphs have same adjacency
                list, False otherwise.

        """
        return self.adjacency_dict == other.adjacency_dict
