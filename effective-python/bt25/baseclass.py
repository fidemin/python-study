
class BaseClass(object):
    def __init__(self, value):
        self.value = value


class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


class OneWay(BaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        BaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


if __name__ == "__main__":
    foo = OneWay(5)
    print(foo.value)
