
def sort_priority(values, group):
    def helper(item):
        if item in group:
            return (0, item)

        return (1, item)

    return sorted(values, key=helper)


def sort_priority2(values, group):
    found = False
    def helper(item):
        if item in group:
            found = True
            return (0, item)

        return (1, item)

    return sorted(values, key=helper), found


def sort_priority3(values, group):
    found = False
    def helper(item):
        nonlocal found
        if item in group:
            found = True
            return (0, item)

        return (1, item)

    return sorted(values, key=helper), found

class Sorter(object):
    def __init__(self, group):
        self._group = group
        self._found = False

    def __call__(self, item):
        if item in self._group:
            self._found = True
            return (0, item)
        return (1, item)

if __name__ == "__main__":
    lst = [8, 3, 1, 2, 5, 4, 7, 6]
    group = {2, 3, 5, 7}
    lst_sorted = sort_priority(lst, group)
    print(lst_sorted)

    lst_sorted2, found = sort_priority2(lst, group)
    assert found is False

    
    lst_sorted3, found = sort_priority3(lst, group)
    assert found is True

    sorter = Sorter(group)
    lst_sorted4 = sorted(lst, key=sorter)
    print (lst_sorted4)

    assert sorter._found is True
    
    
