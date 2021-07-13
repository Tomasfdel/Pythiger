from typing import TypeVar, Generic, List

from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    id: int
    information: T


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
        result = []
        for neighbour in self.node_predecessors(node) + self.node_successors(node):
            if neighbour not in result:
                result.append(neighbour)
        return result

    def node_goes_to(self, origin: Node[T], destination: Node[T]) -> bool:
        return destination.id in self.out_edges[origin.id]

    def node_degree(self, node: Node[T]) -> int:
        return len(self.node_predecessors(node)) + len(self.node_successors(node))
