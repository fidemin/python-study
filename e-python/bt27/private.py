
class MyObject(object):
    def __init__(self):
        self.__value = 71


if __name__ == "__main__":
    a = MyObject()
    print(a.__dict__)
    print(a._MyObject__value)
