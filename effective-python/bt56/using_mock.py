from mock import MagicMock

class RealClass(object):
    def method1(a):
        return a


thing = RealClass()
thing.method1 = MagicMock(return_value=3)
returned_value = thing.method1(3)
assert returned_value == 3
thing.method1.assert_called_with(3)
