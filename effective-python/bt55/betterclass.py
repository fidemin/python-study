
class BetterClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterClass(%d, %d)' % (self.x, self.y)


if __name__ == '__main__':
    c = BetterClass(1, 2)
    print(c)
    print(c.__dict__)
