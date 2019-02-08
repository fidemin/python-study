import json

class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for k, v in instance_dict.items():
            output[k] = self._traverse(k, v)
        return output

    def _traverse(self, key, value):
        if isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, v) for v in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left = None, right = None, parent = None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if isinstance(value, BinaryTreeWithParent) and key == 'parent':
            return value.value
        return super()._traverse(key, value)


class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        # data: json string
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines
        ]


class Switch(object):
    def __init__(self, ports, speed):
        self.ports = ports
        self.speed = speed


class Machine(object):
    def __init__(self, cores, ram, disk):
        self.cores = cores
        self.ram = ram
        self.disk = disk


if __name__ == "__main__":
    from pprint import pprint
    tree = BinaryTree(10, left=BinaryTree(7, right=BinaryTree(9)),
                      right=BinaryTree(13, left=BinaryTree(11)))
    pprint(tree.to_dict())

    root = BinaryTreeWithParent(10)
    root.left = BinaryTreeWithParent(7, parent=root)
    root.left.right = BinaryTreeWithParent(9, parent=root.left)
    pprint(root.to_dict())


    serialized = """{
        "switch": {"ports": 5, "speed": 1e9},
        "machines": [
            {"cores": 8, "ram": 32e9, "disk": 5e12},
            {"cores": 4, "ram": 32e7, "disk": 5e12}
        ]
    }"""

    deserialized = DatacenterRack.from_json(serialized)
    roundtrip = deserialized.to_json()
    pprint(roundtrip)
    assert json.loads(serialized) == json.loads(roundtrip)
