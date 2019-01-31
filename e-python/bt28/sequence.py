from collections.abc import Sequence


class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            value = counts.setdefault(item, 0)
            counts[item] = value + 1
        return counts

class TreeNode(Sequence):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def _search(self, count, index):
        return self._search_from_node(self, [count], index)

    def _search_from_node(self, node, count, index):
        print("value:",node.value, "count:", count)

        if count[0] > index:
            return None
        if count[0] == index:
            return node

        result = None 

        if node.left is not None:
            count[0] += 1
            result = self._search_from_node(node.left, count, index)
 
        if result is not None:
            return result

        if node.right is not None:
            count[0] += 1
            result = self._search_from_node(node.right, count, index)

        return result

    def __getitem__(self, index):
        found = self._search(0, index)
        print("found:", found)
        if not found:
            raise IndexError('Index out of range')
        return found.value


    def __len__(self):
        return 1 # 0을 리턴할 시, if에 이 객체를 넣으면 False로 인식한다....


if __name__ == "__main__":
    foo = FrequencyList(['a', 'b', 'a', 'c'])
    print('length: ', len(foo))
    foo.pop()
    if not foo:
        print('foo is None')
    print('after pop: ', repr(foo))
    print('Frequency:', foo.frequency())

    node = TreeNode(
        10,
        left=TreeNode(
            3,
            left=TreeNode(
                4,
                left=TreeNode(5),
                right=TreeNode(6)
            ),
            right=TreeNode(
                2,
                left=TreeNode(1),
                right=TreeNode(2)
            )
        ),right=TreeNode(23)
    )

    if not node:
        print(node)
        print('node is none')

    found = node[8]
    print(found.value)
