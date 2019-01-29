
class BaseClass(object):
    def __init__(self, value):
        print('base')
        self.value = value 
        print('base end')


class TimesTwo(BaseClass):
    def __init__(self, value):
        print('times two')
        super().__init__(value)
        self.value *= 2
        print('times two end')


class PlusFive(BaseClass):
    def __init__(self, value):
        print('plus five')
        super().__init__(value)
        self.value += 5
        print('plus five end')


class GoodWay(TimesTwo, PlusFive):
    def __init__(self, value):
        super().__init__(value)

if __name__ == "__main__":
    from pprint import pprint
    obj = GoodWay(2)
    print(obj.value)
    pprint(GoodWay.mro())
