from collections import defaultdict
from copy import deepcopy


def get_key_with_zero_indegree(indegree: dict[int]):
    """
    Args:
        indegree: key is the node key and value is the indegree of the node

    Returns:
        str: The key of the node with 0 indegree
    """
    start_key = None
    for key, count in indegree.items():
        if count == 0:
            if start_key is not None:
                raise ValueError("Multiple start keys found")
            start_key = key

    if start_key is None:
        raise ValueError("No start key found")

    return start_key


class Node:
    def __init__(self, key, children=None, operation=None, data=None):
        self.key = key
        self.children = children
        self.operation = operation
        self.data = data
        self.is_leaf = False if children else True

    @staticmethod
    def from_data(data):
        return Node(data["key"], None, None, data["data"])

    @staticmethod
    def from_operation(operation):
        return Node(operation["key"], operation["op_targets"], operation["op"])


class BooleanInterpreter:
    def __init__(self, data, operations):
        self._data = data
        self._operations = operations

    def _operate(self, node_dict: dict[str, Node], start_key):
        node = node_dict[start_key]
        if node.is_leaf:
            return node.data

        values = [set(self._operate(node_dict, child)) for child in node.children]

        if node.operation == "AND":
            return list(set.intersection(*values))
        elif node.operation == "OR":
            return list(set.union(*values))
        else:
            raise ValueError("Invalid operation")

    def _calculate_indegree(self) -> dict[str, int]:
        indegree = defaultdict(int)

        for d in self._data:
            indegree[d["key"]] = 0

        for operation in self._operations:
            if operation["key"] not in indegree:
                indegree[operation["key"]] = 0

            for v in operation["op_targets"]:
                indegree[v] += 1

        return indegree

    def _set_node_dict(self):
        node_dict = {}
        for d in self._data:
            node_dict[d["key"]] = Node.from_data(d)

        for operation in self._operations:
            node_dict[operation["key"]] = Node.from_operation(operation)

        return node_dict

    def expr(self):
        indegree = self._calculate_indegree()

        node_dict: dict[str, Node] = self._set_node_dict()

        start_key = get_key_with_zero_indegree(indegree)

        return self._operate(node_dict, start_key)

    def _build_operation_tree(self, node_dict: dict[str, Node], start_key):
        node = node_dict[start_key]
        if node.is_leaf:
            copied_node_data = deepcopy(node.data)
            return {"data": copied_node_data}

        values = [
            self._build_operation_tree(node_dict, child) for child in node.children
        ]
        return {
            "op_targets": values,
            "op": node.operation,
        }

    def build_operation_tree(self):
        indegree = self._calculate_indegree()

        node_dict: dict[str, Node] = self._set_node_dict()

        start_key = get_key_with_zero_indegree(indegree)

        return self._build_operation_tree(node_dict, start_key)
