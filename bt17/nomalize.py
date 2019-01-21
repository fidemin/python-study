

def normalize(numbers):
    total = sum(numbers)

    result = []
    for value in numbers:
        result.append(value / total * 100)

    return result

def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):
        raise TypeError("iterator is not accepted")
    total = sum(numbers)

    result = []
    for value in numbers:
        result.append(value / total * 100)

    return result


def normalize_func(iter_func):
    total = sum(iter_func())

    result = []
    for value in iter_func():
        result.append(value / total * 100)

    return result


def read_visits(file_path):
    with open(file_path) as f:
        for line in f:
            yield int(line)

class ReadVisit(object):
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path) as f:
            for line in f:
                yield int(line)


if __name__ == "__main__":
    visits = [15, 35, 80]
    percentages = normalize(visits)
    print(percentages)

    path = "./visits.txt"
    visits = read_visits(path)
    percentages = normalize(visits)
    print(percentages)

    percentages = normalize_func(lambda: read_visits(path)) # 람다로 감싸서 넘겨준다.
    print(percentages)

    visit = ReadVisit(path)
    percentages = normalize_defensive(visit)
    print(percentages)
    
