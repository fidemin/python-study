
from collections import defaultdict

def log_missing():
    print('Key added')
    return 0

class MissingCounter(object):
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return 0
 


if __name__ == "__main__":
    current = {'orange': 12, 'blue': 3}

    increments = [
        ('red', 5),
        ('blue', 17),
        ('orange', 9),
    ]

    result = defaultdict(log_missing, current)
    print('Before:', dict(result))
    for key, amount in increments:
        result[key] += amount

    print('After:', dict(result))

    counter = MissingCounter()
    result = defaultdict(counter, current)

    print('Before:', dict(result))
    for key, amount in increments:
        result[key] += amount

    print('After:', dict(result))

