from collections import deque
from typing import List, Dict

from personal_practice.graph.node import Node

global_strategy_dict = {}


class ExecutionStrategy:
    def __init__(self, strategy: str, nodes: List[Node]):
        self.strategy = strategy
        self.nodes = nodes

        for node in nodes:
            global_strategy_dict[node.key] = self

    def add_node(self, node: Node):
        self.nodes.append(node)
        global_strategy_dict[node.key] = self


def graph_from_edges(edges: List[List[str]]) -> Dict[str, Node]:
    """
    Create a graph from a 2D array.

    Args:
        edges (List[List[int]]): A list of lists representing the edges of the graph.

    Returns:
        List[Node]: A list of nodes representing the graph.
    """

    graph = {}
    for edge in edges:
        if edge[0] not in graph:
            graph[edge[0]] = Node(edge[0], edge[0])

        if edge[1] not in graph:
            graph[edge[1]] = Node(edge[1], edge[1])

        graph[edge[0]].add_child(graph[edge[1]])
    return graph


def ingress_from_graph(graph: Dict[str, Node]) -> Dict[str, int]:
    """
    Get the ingress of each node in the graph.

    Args:
        graph (Dict[str, Node]): A graph represented as a dictionary.

    Returns:
        Dict[str, int]: A dictionary with the node key as the key and the ingress as the value.
    """

    return {key: node.ingress() for key, node in graph.items()}


if __name__ == "__main__":
    this_edges = [
        ["ROOT", "A"],
        ["ROOT", "E"],
        ["A", "B"],
        ["B", "C"],
        ["C", "F"],
        ["A", "D"],
        ["E", "D"],
        ["D", "F"],
    ]
    graph = graph_from_edges(this_edges)
    print("graph:", graph)
    ingress_dict = ingress_from_graph(graph)
    print("ingress:", ingress_dict)

    queue = deque()
    for key, ingress in ingress_dict.items():
        if ingress == 0:
            queue.append(key)

    if len(queue) > 1:
        raise ValueError("Multiple roots found.")

    while queue:
        key = queue.popleft()
        print(key)

        node = graph[key]

        if key not in global_strategy_dict:
            ExecutionStrategy("sequential", [node])

        if not node.children:
            continue

        if len(node.children) > 1:
            ExecutionStrategy(
                "parallel",
                [
                    ExecutionStrategy("sequential", [child_node])
                    for child_node in node.children
                ],
            )
        else:
            execution_strategy = global_strategy_dict[node.key]

        for child in node.children:
            ingress_dict[child.key] -= 1

            if ingress_dict[child.key] == 0:
                queue.append(child.key)
