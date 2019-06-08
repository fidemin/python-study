
from unittest.mock import patch

from real import sum_

class MockClass(object):
    def sum(self, a, b):
        return 10

@patch('real.Sum', MockClass)
def test_sum():
    assert sum_(1, 8) == 10


if __name__ == '__main__':
    test_sum()
