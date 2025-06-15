from personal_practice.graph.node import Node


class TestNode:
    def test_init(self):
        key = "key"
        value = "value"
        node = Node(key, value)

        assert node.children == []
        assert node.parents == []
        assert node.key == key
        assert node.value == value

    def test_add_child(self):
        node = Node("parent_key", "parent")
        child = Node("child_key", "child")

        node.add_child(child)

        assert node.children == [child]
        assert child.parents == [node]

    def test_ingress(self):
        node = Node("parent_key", "parent")
        child = Node("child_key", "child")

        node.add_child(child)

        assert node.ingress() == 0
        assert child.ingress() == 1
