from typing import TypeVar, Generic, List

from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    id: int
    information: T


# TODO: Many of these methods are not used in liveness analysis. Consider deleting them.
# TODO: Consider defining a add_undirected_edge and remove_undirected_edge.
class Graph(Generic[T]):
    def __init__(self):
        self.nodes = []
        self.in_edges = []
        self.out_edges = []

    def add_node(self, information: T) -> Node[T]:
        node = Node(len(self.nodes), information)
        self.nodes.append(node)
        self.in_edges.append(set())
        self.out_edges.append(set())
        return node

    def get_nodes(self) -> List[Node[T]]:
        return self.nodes

    def add_edge(self, origin: Node[T], destination: Node[T]):
        self.out_edges[origin.id].add(destination.id)
        self.in_edges[destination.id].add(origin.id)

    def remove_edge(self, origin: Node[T], destination: Node[T]):
        self.out_edges[origin.id].remove(destination.id)
        self.in_edges[destination.id].remove(origin.id)

    def node_successors(self, node: Node[T]) -> List[Node[T]]:
        return [self.nodes[successor_id] for successor_id in self.out_edges[node.id]]

    def node_predecessors(self, node: Node[T]) -> List[Node[T]]:
        return [self.nodes[predecessor_id] for predecessor_id in self.in_edges[node.id]]

    def node_adjacent(self, node: Node[T]) -> List[Node[T]]:
        adjacent_ids = self.in_edges[node.id].union(self.out_edges[node.id])
        return [self.nodes[id] for id in adjacent_ids]

    def node_goes_to(self, origin: Node[T], destination: Node[T]) -> bool:
        return destination.id in self.out_edges[origin.id]

    def are_nodes_adjacent(self, node1: Node[T], node2: Node[T]) -> bool:
        return self.node_goes_to(node1, node2) or self.node_goes_to(node2, node1)

    def node_degree(self, node: Node[T]) -> int:
        return len(self.node_predecessors(node)) + len(self.node_successors(node))
