from weakref import WeakKeyDictionary

class Soldier(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not (-100 <= value <= 100):
            raise ValueError('x position should be between -100, 100')
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not (-100 <= value <= 100):
            raise ValueError('y position should be between -100, 100')
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if not (-100 <= value <= 100):
            raise ValueError('y position should be between -100, 100')
        self._z = z

    def __str__(self):
        return "%s(x=%d, y=%d, z=%d)" % (self.__class__.__name__, self._x, self._y, self._z)


class PosDescriptor(object):
    def __init__(self, *, name, lower=-100, upper=100):
        self._name = name
        self._lower = lower
        self._upper = upper
        self._values = WeakKeyDictionary()

    def __get__(self, instance, klass):
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (self._lower <= value <= self._upper):
            raise ValueError('%s position should be between -100, 100' % self._name)
        self._values[instance] = value


class UpgradedSoldier(object):
    x = PosDescriptor(name='x', lower=-200, upper=200)
    y = PosDescriptor(name='y')
    z = PosDescriptor(name='z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "%s(x=%d, y=%d, z=%d)" % (self.__class__.__name__, self.x, self.y, self.z)


def make_soldier(x, y, z):
    soldier = UpgradedSoldier(x, y, z)

if __name__ == "__main__":
    s1 = Soldier(0, 0, 0)
    print(s1)

    try:
        s1.x = 200
    except ValueError as e:
        print('wrong position: %s' % e)

    us1 = UpgradedSoldier(0, 0, 0)
    print(us1)

    try:
        us1.x = 200
    except ValueError as e:
        print('wrong position: %s' % e)

    make_soldier(0, 0, 0)

    print('---- all soldiers ---')
    for soldier in UpgradedSoldier.__dict__['x']._values.keys():
        print(soldier)
