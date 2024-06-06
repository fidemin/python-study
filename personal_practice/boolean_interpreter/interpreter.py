from collections import defaultdict
from copy import deepcopy
from typing import Optional, List


def get_key_with_zero_indegree(indegree: dict[str, int]):
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
        if children is None:
            children = []
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
    def __init__(self, data):
        self._data: dict = data
        self._sorted_keys: List[str] = []
        self._indegree: Optional[dict[str, int]] = None
        self._node_dict: Optional[dict[str, Node]] = None
        self._start_key: Optional[str] = None
        self._result_cache: dict[str, List[str]] = {}
        self._setup()

    def expr(self):
        return self._operate()

    def build_operation_tree(self):
        return self._build_operation_tree(self._node_dict, self._start_key)

    def build_sorted_keys(self):
        return self._topological_sort(self._indegree, self._node_dict, self._start_key)

    def _setup(self):
        self._set_indegree()
        self._set_node_dict()
        if self._start_key is None:
            self._start_key = get_key_with_zero_indegree(self._indegree)

    def _operate(self):
        if not self._sorted_keys:
            self.build_sorted_keys()

        for key in self._sorted_keys:
            node = self._node_dict[key]
            if node.is_leaf:
                self._result_cache[key] = node.data
            else:
                values = [set(self._result_cache[child]) for child in node.children]
                if node.operation == "AND":
                    self._result_cache[key] = list(set.intersection(*values))
                elif node.operation == "OR":
                    self._result_cache[key] = list(set.union(*values))
                else:
                    raise ValueError("Invalid operation")

        return self._result_cache[self._start_key]

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

    def _set_indegree(self):
        if self._indegree is not None:
            return
        indegree = defaultdict(int)

        for d in self._data:
            key = d["key"]
            operation = d["operation"]

            indegree[key] = 0

            if operation is not None:
                for v in operation["targets"]:
                    indegree[v] += 1
        self._indegree = indegree

    def _set_node_dict(self):
        if self._node_dict is not None:
            return

        node_dict = {}
        for d in self._data:
            key = d["key"]
            operation = d["operation"]
            operation_type = None
            operation_targets = None
            data = d["data"]

            if operation is not None:
                operation_type = operation["type"]
                operation_targets = operation["targets"]

            node_dict[key] = Node(key, operation_targets, operation_type, data)

        self._node_dict = node_dict

    def _topological_sort(
        self, indegree: dict[str, int], node_dict: dict[str, Node], start_key: str
    ):
        queue = [start_key]
        # deepcopy indegree to avoid modifying the original indegree
        indegree = deepcopy(indegree)
        while queue:
            key = queue.pop(0)
            self._sorted_keys.append(key)

            for child in node_dict[key].children:
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

        for count in indegree.values():
            if count != 0:
                raise ValueError("Wrong indegree or Cycle detected")
        self._sorted_keys.reverse()
        return self._sorted_keys
