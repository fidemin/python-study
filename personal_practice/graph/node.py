class Node:
    def __init__(self, key, value):
        self.children = []
        self.parents = []
        self.key = key
        self.value = value

    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)

    def ingress(self):
        return len(self.parents)

    def __str__(self):
        return self._to_str()

    def __repr__(self):
        return self._to_str()

    def _to_str(self):
        children_keys = [child.key for child in self.children]
        parents_keys = [parent.key for parent in self.parents]
        return f"Node(key={self.key}, value={self.value}, children={children_keys}, parents={parents_keys})"
